"""Build the static site: one page per language plus a page per town.

Source: src/template.html (English text + translations in the T object of its script).
Run from the repository root:  python3 tools/build.py
"""
import json, re, subprocess, pathlib, html, copy, urllib.parse
from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = 'https://virginierealestate.com'
LANGS = ['en', 'nl', 'fr', 'pt']
TEMPLATE = (ROOT / 'src/template.html').read_text(encoding='utf-8')

# ---- translations from the template's script ----------------------------------
def load_T():
    i = TEMPLATE.index('const T = {')
    j = TEMPLATE.index('\n};', i) + 3
    js = TEMPLATE[i:j] + '\nprocess.stdout.write(JSON.stringify(T));'
    return json.loads(subprocess.run(['node', '-e', js], capture_output=True, text=True, check=True).stdout)

T = load_T()

META = {
    'en': dict(title="Virginie Real Estate | Real estate agent and buyer's agent on the Silver Coast, Portugal",
               desc="Virginie Verschaete, real estate agent and buyer's agent on Portugal's Silver Coast: Caldas da Rainha, Óbidos, Foz do Arelho, São Martinho do Porto, Alcobaça, Bombarral and Lourinhã. Buying, selling, new builds and land. English, Dutch, French and Portuguese."),
    'nl': dict(title="Virginie Real Estate | Makelaar en aankoopmakelaar aan de Zilverkust, Portugal",
               desc="Virginie Verschaete, Belgische makelaar en aankoopmakelaar aan de Portugese Zilverkust: Caldas da Rainha, Óbidos, Foz do Arelho, São Martinho do Porto, Alcobaça, Bombarral en Lourinhã. Kopen, verkopen, nieuwbouw en bouwgrond. In het Nederlands, Frans, Engels en Portugees."),
    'fr': dict(title="Virginie Real Estate | Agente immobilière et agente de l'acheteur sur la Silver Coast, Portugal",
               desc="Virginie Verschaete, agente immobilière et agente de l'acheteur sur la Silver Coast au Portugal : Caldas da Rainha, Óbidos, Foz do Arelho, São Martinho do Porto, Alcobaça, Bombarral et Lourinhã. Achat, vente, neuf et terrains. En français, néerlandais, anglais et portugais."),
    'pt': dict(title="Virginie Real Estate | Consultora imobiliária e consultora do comprador na Costa de Prata",
               desc="Virginie Verschaete, consultora imobiliária e consultora do comprador na Costa de Prata: Caldas da Rainha, Óbidos, Foz do Arelho, São Martinho do Porto, Alcobaça, Bombarral e Lourinhã. Compra, venda, construção nova e terrenos. Em português, inglês, francês e neerlandês."),
}

LISTINGS = 'https://www.iadportugal.pt/en/real-estate-agent/virginie.verschaete'

def url(lang, path=''):
    return f"{SITE}/{'' if lang == 'en' else lang + '/'}{path}"

def hreflang_tags(path):
    tags = [f'<link rel="alternate" hreflang="{l}" href="{url(l, path)}">' for l in LANGS]
    tags.append(f'<link rel="alternate" hreflang="x-default" href="{url("en", path)}">')
    return '\n'.join(tags)

# ---- towns ----------------------------------------------------------------------
TOWNS = json.loads((ROOT / 'src/towns.json').read_text(encoding='utf-8'))

# ---- helpers --------------------------------------------------------------------
def set_head(soup, lang, title, desc, path, depth):
    soup.html['lang'] = lang
    soup.title.string = title
    soup.find('meta', attrs={'name': 'description'})['content'] = desc
    for prop, val in [('og:title', title), ('og:description', desc), ('og:url', url(lang, path))]:
        tag = soup.find('meta', attrs={'property': prop})
        if tag: tag['content'] = val
    soup.find('link', rel='canonical')['href'] = url(lang, path)
    for old in soup.find_all('link', rel='alternate'): old.decompose()
    soup.find('link', rel='canonical').insert_after(BeautifulSoup(hreflang_tags(path), 'html.parser'))
    og_locale = {'en': 'en_GB', 'nl': 'nl_BE', 'fr': 'fr_BE', 'pt': 'pt_PT'}[lang]
    loc = soup.find('meta', attrs={'property': 'og:locale'})
    if not loc:
        loc = soup.new_tag('meta'); loc['property'] = 'og:locale'
        soup.find('meta', attrs={'property': 'og:url'}).insert_after(loc)
    loc['content'] = og_locale

def fix_assets(soup, depth):
    pre = '../' * depth
    if not pre: return
    for tag in soup.find_all(['img', 'link', 'a']):
        for attr in ('src', 'href'):
            v = tag.get(attr)
            if v and v.startswith('img/'): tag[attr] = pre + v

def lang_links(soup, lang, path, depth):
    pre = '../' * depth
    for a in soup.select('.langs .lng'):
        l = a['data-lang']
        target = (pre + ('' if l == 'en' else l + '/') + path) or './'
        a['href'] = target
        a['hreflang'] = l
        if l == lang: a['aria-current'] = 'page'
        elif a.has_attr('aria-current'): del a['aria-current']

def translate(soup, lang):
    if lang == 'en': return
    d = T[lang]
    for el in soup.select('[data-i18n]'):
        k = el['data-i18n']
        if k in d:
            el.clear(); el.append(BeautifulSoup(d[k], 'html.parser'))

def listings(soup):
    for a in soup.select('.js-listings'):
        a['href'] = LISTINGS; a['target'] = '_blank'; a['rel'] = 'noopener'

def faq_jsonld(soup):
    faq = []
    for i in range(1, 20):
        q = soup.find(attrs={'data-i18n': f'q{i}'}); a = soup.find(attrs={'data-i18n': f'a{i}'})
        if not q or not a: break
        faq.append({'@type': 'Question', 'name': q.get_text(' ', strip=True),
                    'acceptedAnswer': {'@type': 'Answer', 'text': a.get_text(' ', strip=True)}})
    return faq

def set_jsonld(soup, graph):
    tag = soup.find('script', type='application/ld+json')
    tag.string = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False)

def base_org(soup):
    g = json.loads(soup.find('script', type='application/ld+json').string)['@graph']
    return [x for x in g if x.get('@type') == 'RealEstateAgent'][0]

# ---- home pages -----------------------------------------------------------------
def build_home(lang):
    soup = BeautifulSoup(TEMPLATE, 'html.parser')
    depth = 0 if lang == 'en' else 1
    translate(soup, lang)
    set_head(soup, lang, META[lang]['title'], META[lang]['desc'], '', depth)
    org = base_org(soup); org['url'] = url(lang)
    set_jsonld(soup, [org, {'@type': 'FAQPage', 'inLanguage': lang, 'mainEntity': faq_jsonld(soup)}])
    fix_assets(soup, depth); lang_links(soup, lang, '', depth); listings(soup)
    out = ROOT / ('index.html' if lang == 'en' else f'{lang}/index.html')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(str(soup), encoding='utf-8')

# ---- town pages -----------------------------------------------------------------
def build_town(lang, slug, t):
    L = TOWNS['labels'][lang]; tt = t[lang]
    path = f'areas/{slug}/'
    depth = (0 if lang == 'en' else 1) + 2
    soup = BeautifulSoup(TEMPLATE, 'html.parser')
    translate(soup, lang)
    main = soup.find('main')
    others = ''.join(f'<a href="../{s}/">{TOWNS["towns"][s]["name"]}</a>' for s in TOWNS['order'] if s != slug)
    bullets = ''.join(f'<li>{html.escape(b)}</li>' for b in tt['facts'])
    home = '../../'
    main.clear()
    main.append(BeautifulSoup(f'''
<section class="hero town-hero">
  <div class="wrap">
    <div class="crumbs"><a href="{home}">{L['home']}</a> / <a href="{home}#areas">{L['areas']}</a> / <span>{t["name"]}</span></div>
    <div class="eyebrow">{L['eyebrow']}</div>
    <h1>{html.escape(tt['h1'])}</h1>
    <p class="lead">{html.escape(tt['intro'])}</p>
  </div>
</section>
<section class="town-body">
  <div class="wrap guide-grid">
    <div>
      <div class="eyebrow">{L['good']}</div>
      <ul class="facts-list">{bullets}</ul>
    </div>
    <div class="town-cta">
      <h2>{html.escape(tt['cta_title'])}</h2>
      <p>{html.escape(L['cta_p'])}</p>
      <div class="ctas">
        <a class="btn solid" href="https://wa.me/351920445059?text={urllib.parse.quote(tt['wa'])}"><span>{L['cta_wa']}</span><span class="arr">→</span></a>
        <a class="btn ghost" href="{LISTINGS}" target="_blank" rel="noopener">{L['cta_sale']}</a>
      </div>
      <p class="more-links"><a href="{home}#buyers-agent">{L['ba']}</a> · <a href="{home}#guide">{L['guide']}</a></p>
    </div>
  </div>
</section>
<section class="cream town-others">
  <div class="wrap"><div class="eyebrow">{L['others']}</div><div class="other-towns">{others}</div></div>
</section>''', 'html.parser'))
    # header links point back to the home page sections
    for a in soup.select('header nav a[href^="#"]'): a['href'] = home + a['href']
    logo = soup.select_one('header a.logo');  logo['href'] = home
    title = f"{tt['h1']} | Virginie Real Estate"
    set_head(soup, lang, title, tt['meta'], path, depth)
    org = base_org(soup); org['url'] = url(lang)
    place = {'@type': 'WebPage', 'name': tt['h1'], 'url': url(lang, path), 'inLanguage': lang,
             'about': {'@type': 'Place', 'name': f"{t['name']}, Portugal"},
             'breadcrumb': {'@type': 'BreadcrumbList', 'itemListElement': [
                 {'@type': 'ListItem', 'position': 1, 'name': L['home'], 'item': url(lang)},
                 {'@type': 'ListItem', 'position': 2, 'name': t['name'], 'item': url(lang, path)}]},
             'publisher': {'@type': 'RealEstateAgent', 'name': 'Virginie Real Estate'}}
    set_jsonld(soup, [org, place])
    fix_assets(soup, depth); lang_links(soup, lang, path, depth)
    # remove the WhatsApp/page script parts that expect home sections: keep script, it is harmless
    out = ROOT / ((f'{lang}/' if lang != 'en' else '') + path + 'index.html')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(str(soup), encoding='utf-8')

# ---- sitemap & llms.txt ---------------------------------------------------------
def sitemap(paths):
    rows = []
    for p in paths:
        alts = ''.join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{url(l, p)}"/>' for l in LANGS)
        for l in LANGS:
            rows.append(f'  <url><loc>{url(l, p)}</loc>{alts}</url>')
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
           + '\n'.join(rows) + '\n</urlset>\n')
    (ROOT / 'sitemap.xml').write_text(xml, encoding='utf-8')

def llms():
    src = (ROOT / 'src/llms.txt').read_text(encoding='utf-8')
    pages = '\n'.join(f"- [{TOWNS['towns'][s]['en']['h1']}]({url('en', f'areas/{s}/')})" for s in TOWNS['order'])
    langs = '\n'.join(f'- {n}: {url(l)}' for l, n in [('en', 'English'), ('nl', 'Nederlands'), ('fr', 'Français'), ('pt', 'Português')])
    (ROOT / 'llms.txt').write_text(src + f'\n## Pages\n{langs}\n\n## Area guides\n{pages}\n', encoding='utf-8')

if __name__ == '__main__':
    for l in LANGS:
        build_home(l)
        for s in TOWNS['order']:
            build_town(l, s, TOWNS['towns'][s])
    sitemap([''] + [f'areas/{s}/' for s in TOWNS['order']])
    llms()
    print('built', len(LANGS) * (1 + len(TOWNS['order'])), 'pages')
