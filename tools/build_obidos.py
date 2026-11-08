#!/usr/bin/env python3
"""Hidden (unlisted, noindex) page about the villas in Óbidos, in EN and PT.
Output: obidos-villas-k7m2q/index.html (EN) and obidos-villas-k7m2q/pt/index.html (PT).
Not linked from the site and not in the sitemap."""
import os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = "obidos-villas-k7m2q"
MAPS = "https://maps.app.goo.gl/zax1ATeGUjuHwDj4A"
PHONE = "+351 920 445 059"
WA = "351920445059"

# Available villas (payment plans, phase 2; sold: L2-L6, L13, L15)
VILLAS = [
    # lot, type key, plot m2, construction m2, price
    (1, "single", 442, 144.95, 419000),
    (7, "two", 431, 166.30, 479000),
    (8, "two", 345, 154.85, 439000),
    (9, "two", 361, 152.25, 439000),
    (10, "semi", 289, 155.30, 439000),
    (11, "semi", 262, 155.30, 439000),
    (12, "single", 554, 159.85, 479000),
    (14, "single", 467, 148.45, 449000),
    (16, "single", 471, 157.05, 479000),
]

T = {
 "en": dict(
  lang="en", other="pt", other_label="Português", title="Contemporary villas in Óbidos | Virginie Real Estate",
  eyebrow="Óbidos · Silver Coast", h1="Contemporary villas in Óbidos",
  intro=["A small development of contemporary three-bedroom villas with a private pool, in Bairro da Senhora da Luz, Óbidos. Five minutes from the walled town of Óbidos and from Caldas da Rainha, close to the Óbidos Lagoon and the beaches of Foz do Arelho, and about an hour from Lisbon.",
         "Each villa has three bedrooms and three bathrooms, an open living area with a fully equipped kitchen, a private garden and terrace, a barbecue area and covered parking. Built with the Plastbau system for thermal and acoustic insulation, with photovoltaic panels, solar hot water and pre-installation for air conditioning. Expected energy rating A+. You choose your finishes within a set allowance per category."],
  done_t="Expected completion", done="End of 2027",
  loc_t="Location", loc="Bairro da Senhora da Luz, Óbidos", map_btn="Open in Google Maps",
  avail_t="Available villas", avail_p="Nine villas are available. Each monograph contains the location, the plot plan, the floor plans, the elevations and 3D views.",
  th=["Villa", "Type", "Plot", "Construction", "Price", "Monograph"],
  types={"single": "Single level", "two": "Two floors", "semi": "Semi-detached, two floors"},
  dl="PDF", price_note="Prices include VAT on the construction.",
  pay_t="Payment plan", pay_p="You buy the plot and sign a separate construction contract. Payments follow the progress of the works:",
  stages=[("1%", "Reservation"), ("4%", "Promissory contract (CPCV)"), ("20%", "Deed of the plot"), ("25%", "Structure complete"), ("20%", "Finishing phase 1: roof, wall finishes, floors, tiles and stone"), ("20%", "Finishing phase 2: painting, kitchen, bathrooms, joinery, electrical fittings, pool and exterior"), ("10%", "Habitation licence")],
  tax="Because the plot and the construction are bought separately, IMT and stamp duty are paid on the value of the plot (20% of the total price), not on the construction. Always confirm the taxes for your situation with your lawyer.",
  pay_dl="Payment plan per villa (Excel)",
  docs_t="Documents", docs=[("files/finishes-specifications-EN.pdf", "Specifications & finishes", "PDF, English"), ("files/moradias-obidos-PT.pdf", "Overview of the villas", "PDF, Portuguese"), ("files/payment-plans-villas-obidos.xlsx", "Payment plan per villa", "Excel, English and Portuguese")],
  note="The villa design is a proposal and is still subject to submission and approval by the Câmara Municipal de Óbidos. Images, plans and areas are illustrative. Prices, availability and the completion date may change; please confirm before reserving.",
  c_t="Interested in one of the villas?", c_p="I'm happy to send more information, answer your questions or arrange a visit to the plots. I reply within 24 hours.",
  wa_btn="WhatsApp", wa_msg="Hello Virginie, I'd like more information about the villas in Óbidos.",
 ),
 "pt": dict(
  lang="pt-PT", other="en", other_label="English", title="Moradias contemporâneas em Óbidos | Virginie Real Estate",
  eyebrow="Óbidos · Costa de Prata", h1="Moradias contemporâneas em Óbidos",
  intro=["Um pequeno loteamento de moradias T3 contemporâneas com piscina privada, no Bairro da Senhora da Luz, em Óbidos. A cinco minutos da vila de Óbidos e de Caldas da Rainha, perto da Lagoa de Óbidos e das praias da Foz do Arelho, e a cerca de uma hora de Lisboa.",
         "Cada moradia tem três quartos e três casas de banho, sala ampla aberta para a cozinha totalmente equipada, jardim privado e terraço, zona de churrasco e estacionamento coberto. Construção pelo sistema Plastbau, com isolamento térmico e acústico, painéis fotovoltaicos, água quente solar e pré-instalação de ar condicionado. Classificação energética prevista A+. Os acabamentos são escolhidos pelo comprador, dentro de um orçamento por categoria."],
  done_t="Conclusão prevista", done="Final de 2027",
  loc_t="Localização", loc="Bairro da Senhora da Luz, Óbidos", map_btn="Abrir no Google Maps",
  avail_t="Moradias disponíveis", avail_p="Estão disponíveis nove moradias. Cada monografia inclui a localização, a implantação no lote, as plantas, os alçados e imagens 3D.",
  th=["Moradia", "Tipo", "Lote", "Construção", "Preço", "Monografia"],
  types={"single": "Térrea", "two": "Dois pisos", "semi": "Geminada, dois pisos"},
  dl="PDF", price_note="Preços com IVA incluído na construção.",
  pay_t="Plano de pagamento", pay_p="Compra o lote e assina um contrato de empreitada separado. Os pagamentos acompanham o andamento da obra:",
  stages=[("1%", "Reserva"), ("4%", "Contrato-promessa (CPCV)"), ("20%", "Escritura do lote"), ("25%", "Estrutura concluída"), ("20%", "Acabamentos fase 1: cobertura, acabamentos de paredes, pavimentos, cerâmicos e pedras"), ("20%", "Acabamentos fase 2: pinturas, cozinha, casas de banho, carpintarias, aparelhagem elétrica, piscina e exteriores"), ("10%", "Licença de utilização")],
  tax="Como o lote e a construção são adquiridos separadamente, o IMT e o Imposto do Selo são pagos sobre o valor do lote (20% do preço total), e não sobre a construção. Confirme sempre os impostos aplicáveis à sua situação com o seu advogado.",
  pay_dl="Plano de pagamento por moradia (Excel)",
  docs_t="Documentos", docs=[("files/finishes-specifications-EN.pdf", "Especificações e acabamentos", "PDF, inglês"), ("files/moradias-obidos-PT.pdf", "Apresentação das moradias", "PDF, português"), ("files/payment-plans-villas-obidos.xlsx", "Plano de pagamento por moradia", "Excel, inglês e português")],
  note="O projeto de moradia é uma proposta, ainda sujeita a submissão e aprovação pela Câmara Municipal de Óbidos. Imagens, plantas e áreas são meramente ilustrativas. Preços, disponibilidade e data de conclusão podem ser alterados; confirme antes de reservar.",
  c_t="Interessado numa das moradias?", c_p="Terei todo o gosto em enviar mais informação, responder às suas perguntas ou marcar uma visita aos lotes. Respondo no prazo de 24 horas.",
  wa_btn="WhatsApp", wa_msg="Olá Virginie, gostaria de receber mais informação sobre as moradias em Óbidos.",
 ),
}

CSS = """
@font-face{font-family:"Lora";src:url({F}fonts/lora.woff) format("woff");font-weight:400 700;font-display:swap}
@font-face{font-family:"Lora";src:url({F}fonts/lora-italic.woff) format("woff");font-style:italic;font-weight:400 700;font-display:swap}
@font-face{font-family:"Jost";src:url({F}fonts/jost.woff) format("woff");font-weight:300 600;font-display:swap}
:root{--ink:#1d1d1f;--text:#4a4843;--gold:#c6a978;--gold-text:#94763f;--cream:#f6f2ea;--line:rgba(178,147,80,.35);--display:"Lora",Georgia,serif;--body:"Jost","Helvetica Neue",Arial,sans-serif}
*{box-sizing:border-box;margin:0;padding:0}
body{font:400 16px/1.75 var(--body);color:var(--text);background:#fff;-webkit-font-smoothing:antialiased}
h1,h2,h3{font-family:var(--display);font-weight:400;color:var(--ink);line-height:1.15}
a{color:inherit}
.wrap{max-width:1180px;margin:0 auto;padding:0 clamp(20px,5vw,56px)}
header{border-bottom:1px solid var(--line);background:#fff}
.bar{display:flex;align-items:center;justify-content:space-between;height:80px;gap:20px}
.bar img{height:50px;width:auto;display:block}
.bar .lang{font:500 12px var(--body);letter-spacing:.14em;text-transform:uppercase;color:var(--gold-text);text-decoration:none}
.eyebrow{font:500 12px var(--body);letter-spacing:.24em;text-transform:uppercase;color:var(--gold-text);display:flex;align-items:center;gap:14px}
.eyebrow::before{content:"";width:36px;height:1px;background:var(--gold)}
section{padding:clamp(56px,8vw,96px) 0}
.cream{background:var(--cream)}
.hero-grid{display:grid;grid-template-columns:6fr 5fr;gap:clamp(32px,6vw,72px);align-items:center}
.hero h1{font-size:clamp(38px,5.4vw,64px);margin:22px 0 24px}
.hero p{margin-bottom:16px;max-width:60ch}
.hero img{width:100%;height:auto;display:block;border:1px solid var(--line);padding:10px;background:#fff}
.facts{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:30px;padding-top:26px;border-top:1px solid var(--line)}
.facts strong{display:block;font:400 22px var(--display);color:var(--ink)}
.facts span{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#7d786f}
.btn{display:inline-flex;align-items:center;gap:10px;font:500 12px var(--body);letter-spacing:.18em;text-transform:uppercase;text-decoration:none;padding:16px 26px;border:1px solid var(--ink);color:var(--ink);background:transparent}
.btn.solid{background:var(--ink);color:#fff}
.btn.gold{background:var(--gold);border-color:var(--gold);color:var(--ink)}
.ctas{display:flex;flex-wrap:wrap;gap:12px;margin-top:26px}
h2{font-size:clamp(30px,3.6vw,42px);margin:16px 0 18px}
.lead{max-width:62ch}
table{width:100%;border-collapse:collapse;margin-top:34px;font-size:15px}
th{font:500 11px var(--body);letter-spacing:.16em;text-transform:uppercase;color:var(--gold-text);text-align:left;padding:0 12px 12px;border-bottom:1px solid var(--ink)}
td{padding:16px 12px;border-bottom:1px solid var(--line);vertical-align:middle}
td.v{font:400 20px var(--display);color:var(--ink);white-space:nowrap}
td.p{white-space:nowrap;color:var(--ink);font-weight:500}
td a{color:var(--gold-text);font-weight:500;text-decoration:none;white-space:nowrap}
td a:hover{text-decoration:underline}
.m{display:none}
.small{font-size:13px;color:#7d786f;margin-top:14px}
.stages{list-style:none;margin-top:28px;display:grid;gap:0;max-width:820px}
.stages li{display:grid;grid-template-columns:90px 1fr;gap:18px;padding:14px 0;border-bottom:1px solid var(--line)}
.stages b{font:400 24px var(--display);color:var(--gold-text)}
.tax{margin-top:26px;max-width:820px;padding:22px 26px;background:#fff;border:1px solid var(--line);font-size:15px}
.docs{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:30px}
.docs a{display:block;text-decoration:none;border:1px solid var(--line);padding:26px;background:#fff;transition:border-color .2s}
.docs a:hover{border-color:var(--gold)}
.docs strong{display:block;font:400 21px var(--display);color:var(--ink);margin-bottom:6px}
.docs span{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold-text)}
.note{font-size:13px;color:#7d786f;max-width:820px;margin-top:30px;padding-top:18px;border-top:1px solid var(--line)}
.contact{background:var(--ink);color:#d8d4cc}
.contact h2{color:#fff}
.contact .btn{border-color:#fff;color:#fff}
.contact .btn.gold{color:var(--ink);border-color:var(--gold)}
.contact p a{color:var(--gold);text-decoration:none}
footer{padding:26px 0;font-size:13px;color:#7d786f;text-align:center}
@media (max-width:960px){.hero-grid{grid-template-columns:1fr}.docs{grid-template-columns:1fr}}
@media (max-width:700px){
 table,thead,tbody,tr,td{display:block}thead{display:none}
 tr{border-bottom:1px solid var(--line);padding:14px 0;display:grid;grid-template-columns:1fr auto;gap:2px 16px}
 td{border:0;padding:2px 0}
 td.v{grid-column:1}td.p{grid-column:2;grid-row:1;text-align:right}
 td.t{grid-column:1/-1;font-size:14px}td.a{grid-column:1/-1;font-size:14px;color:#7d786f}
 td.d{grid-column:1/-1}.m{display:inline}
 .stages li{grid-template-columns:64px 1fr}
 .btn{width:100%;justify-content:center}
}
"""

def eur(v, lang):
    s = f"{v:,.0f}".replace(",", " " if lang == "pt-PT" else ",")
    return f"{s} €" if lang == "pt-PT" else f"€{s}"

def num(v, lang):
    s = (f"{v:.2f}".rstrip("0").rstrip(".")) if isinstance(v, float) else str(v)
    return s.replace(".", ",") if lang == "pt-PT" else s

def page(k, depth):
    d = T[k]; up = "../" * depth; L = d["lang"]
    e = html.escape
    rows = "\n".join(
        f'<tr><td class="v">L{lot}</td><td class="t">{e(d["types"][ty])}</td>'
        f'<td class="a"><span class="m">{e(d["th"][2])}: </span>{num(plot,L)} m²</td><td class="a"><span class="m">{e(d["th"][3])}: </span>{num(area,L)} m²</td>'
        f'<td class="p">{eur(price,L)}</td>'
        f'<td class="d"><a href="{up}files/villa-lot-{lot}-monograph.pdf" target="_blank" rel="noopener">{e(d["dl"])} · L{lot} ↓</a></td></tr>'
        for lot, ty, plot, area, price in VILLAS)
    th = "".join(f"<th>{e(h)}</th>" for h in d["th"])
    stages = "".join(f"<li><b>{p}</b><span>{e(t)}</span></li>" for p, t in d["stages"])
    docs = "".join(f'<a href="{up}{f}" target="_blank" rel="noopener"><strong>{e(t)}</strong><span>{e(s)} ↓</span></a>' for f, t, s in d["docs"])
    intro = "".join(f"<p>{e(p)}</p>" for p in d["intro"])
    other_href = "pt/" if k == "en" else "../"
    wa = f"https://wa.me/{WA}?text=" + __import__("urllib.parse").parse.quote(d["wa_msg"])
    return f"""<!DOCTYPE html>
<html lang="{L}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow, noarchive">
<title>{e(d['title'])}</title>
<link rel="icon" href="{up}../img/favicon.svg" type="image/svg+xml">
<style>{CSS.replace('{F}', up + '../')}</style>
</head>
<body>
<header><div class="wrap bar"><a href="{up}../"><img src="{up}../img/logo-main.svg" alt="Virginie Real Estate" width="190" height="50"></a><a class="lang" href="{other_href}">{e(d['other_label'])}</a></div></header>

<section class="hero cream"><div class="wrap hero-grid">
<div>
<div class="eyebrow">{e(d['eyebrow'])}</div>
<h1>{e(d['h1'])}</h1>
{intro}
<div class="facts"><div><strong>{e(d['done'])}</strong><span>{e(d['done_t'])}</span></div><div><strong>{len(VILLAS)} · T3</strong><span>{e(d['avail_t'])}</span></div></div>
</div>
<img src="{up}files/villas-aerial.jpg" alt="{e(d['h1'])}" width="979" height="551">
</div></section>

<section><div class="wrap">
<div class="eyebrow">{e(d['loc_t'])}</div>
<h2>{e(d['loc'])}</h2>
<div class="ctas"><a class="btn solid" href="{MAPS}" target="_blank" rel="noopener">{e(d['map_btn'])} →</a></div>
</div></section>

<section class="cream"><div class="wrap">
<div class="eyebrow">{e(d['avail_t'])}</div>
<h2>{e(d['avail_t'])}</h2>
<p class="lead">{e(d['avail_p'])}</p>
<table><thead><tr>{th}</tr></thead><tbody>
{rows}
</tbody></table>
<p class="small">{e(d['price_note'])}</p>
</div></section>

<section><div class="wrap">
<div class="eyebrow">{e(d['pay_t'])}</div>
<h2>{e(d['pay_t'])}</h2>
<p class="lead">{e(d['pay_p'])}</p>
<ul class="stages">{stages}</ul>
<p class="tax">{e(d['tax'])}</p>
<div class="ctas"><a class="btn" href="{up}files/payment-plans-villas-obidos.xlsx">{e(d['pay_dl'])} ↓</a></div>
</div></section>

<section class="cream"><div class="wrap">
<div class="eyebrow">{e(d['docs_t'])}</div>
<h2>{e(d['docs_t'])}</h2>
<div class="docs">{docs}</div>
<p class="note">{e(d['note'])}</p>
</div></section>

<section class="contact"><div class="wrap">
<div class="eyebrow">Virginie Real Estate</div>
<h2>{e(d['c_t'])}</h2>
<p class="lead">{e(d['c_p'])}</p>
<p style="margin-top:14px"><a href="tel:+351920445059">{PHONE}</a> · <a href="mailto:info@virginierealestate.com">info@virginierealestate.com</a></p>
<div class="ctas"><a class="btn gold" href="{wa}" target="_blank" rel="noopener">{e(d['wa_btn'])} →</a><a class="btn" href="tel:+351920445059">{PHONE}</a></div>
</div></section>
<footer>© Virginie Real Estate · virginierealestate.com</footer>
</body>
</html>
"""

out = os.path.join(ROOT, SLUG)
os.makedirs(os.path.join(out, "pt"), exist_ok=True)
open(os.path.join(out, "index.html"), "w").write(page("en", 0))
open(os.path.join(out, "pt", "index.html"), "w").write(page("pt", 1))
print("built", SLUG)
