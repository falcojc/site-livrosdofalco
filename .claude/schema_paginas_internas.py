# -*- coding: utf-8 -*-
"""
Gera o JSON-LD das paginas internas: as 5 categorias, o hub /categoria/ e
/arquetipos/. Nenhuma delas tinha uma linha de dado estruturado.

Decisao central: os livros sao referenciados pelo MESMO @id que a home usa
(https://www.livrosdofalco.com.br/#slug), nunca redescritos. Em JSON-LD, o
mesmo @id significa a mesma entidade: o catalogo continua sendo declarado
uma unica vez, e as categorias so apontam. Redescrever criaria trinta livros
homonimos concorrendo entre si no grafo.

Cada pagina recebe:
  - CollectionPage (nome, descricao, ligacao ao WebSite e ao autor)
  - ItemList com as obras da categoria, na ordem em que aparecem na pagina
  - BreadcrumbList (Home > Categorias > esta pagina)

Idempotente: regenera o bloco se ja existir.
Uso: python .claude/schema_paginas_internas.py [--dry-run]
"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BASE = "https://www.livrosdofalco.com.br"
AUTOR_ID = BASE + "/#domenico-falco"
SITE_ID = BASE + "/#website"
MARCA = "<!-- json-ld gerado por .claude/schema_paginas_internas.py -->"

# Ids validos, lidos da home: se um card de categoria usar id que a home nao
# tem, o link do grafo aponta para o vazio e precisa aparecer no relatorio.
home = (RAIZ / "index.html").read_text(encoding="utf-8")
IDS_HOME = set(re.findall(r'<div class="(?:book-card[^"]*|omnibus)" id="([^"]+)">', home))


def texto(t):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t)).strip()


def ler(p):
    h = p.read_text(encoding="utf-8")
    m_t = re.search(r"<title>(.*?)</title>", h, re.S)
    m_d = re.search(r'<meta name="description" content="(.*?)"', h, re.S)
    m_h = re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S)
    return h, {
        "title": texto(m_t.group(1)) if m_t else "",
        "desc": texto(m_d.group(1)) if m_d else "",
        "h1": texto(m_h.group(1)) if m_h else "",
    }


def obras_da_pagina(h):
    """(id, titulo) de cada card, na ordem em que aparecem."""
    out = []
    for m in re.finditer(
        r'<div class="book-card[^"]*" id="([^"]+)">(.*?)(?=<div class="book-card|</section>)',
        h, re.S):
        t = re.search(r"<h3>(.*?)</h3>", m.group(2), re.S)
        out.append((m.group(1), texto(t.group(1)) if t else m.group(1)))
    return out


def breadcrumb(itens):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": nome, "item": url}
            for i, (nome, url) in enumerate(itens, start=1)
        ],
    }


def injetar(p, grafo):
    h = p.read_text(encoding="utf-8")
    bloco = (MARCA + '\n<script type="application/ld+json">\n'
             + json.dumps({"@context": "https://schema.org", "@graph": grafo},
                          ensure_ascii=False, indent=2)
             + "\n</script>\n")
    antigo = re.search(re.escape(MARCA) + r'\s*<script type="application/ld\+json">.*?</script>\s*',
                       h, re.S)
    h = h[:antigo.start()] + bloco + h[antigo.end():] if antigo else h.replace("</head>", bloco + "</head>", 1)
    if "--dry-run" not in sys.argv:
        p.write_text(h, encoding="utf-8")


relatorio, orfas = [], []

# ------------------------------------------------------- 5 paginas de categoria
for p in sorted((RAIZ / "categoria").glob("*/index.html")):
    slug = p.parent.name
    h, meta = ler(p)
    url = f"{BASE}/categoria/{slug}/"
    obras = obras_da_pagina(h)
    for oid, _ in obras:
        if oid not in IDS_HOME:
            orfas.append(f"{slug}:{oid}")
    grafo = [
        {
            "@type": "CollectionPage",
            "@id": url + "#page",
            "url": url,
            "name": meta["h1"] or meta["title"],
            "description": meta["desc"],
            "inLanguage": "pt-BR",
            "isPartOf": {"@id": SITE_ID},
            "about": {"@id": AUTOR_ID},
            "mainEntity": {
                "@type": "ItemList",
                "numberOfItems": len(obras),
                "itemListElement": [
                    {"@type": "ListItem", "position": i,
                     "item": {"@id": f"{BASE}/#{oid}", "@type": "Book", "name": nome}}
                    for i, (oid, nome) in enumerate(obras, start=1)
                ],
            },
        },
        breadcrumb([("Início", BASE + "/"), ("Categorias", BASE + "/categoria/"),
                    (meta["h1"], url)]),
    ]
    injetar(p, grafo)
    relatorio.append((f"categoria/{slug}/", len(obras)))

# ------------------------------------------------------------- hub /categoria/
p = RAIZ / "categoria" / "index.html"
h, meta = ler(p)
cats = []
for slug in sorted(set(re.findall(r'href="/categoria/([a-z-]+)/"', h))):
    ph = RAIZ / "categoria" / slug / "index.html"
    if ph.exists():
        _, m = ler(ph)
        cats.append((slug, m["h1"], m["desc"]))
grafo = [
    {
        "@type": "CollectionPage",
        "@id": BASE + "/categoria/#page",
        "url": BASE + "/categoria/",
        "name": meta["h1"] or meta["title"],
        "description": meta["desc"],
        "inLanguage": "pt-BR",
        "isPartOf": {"@id": SITE_ID},
        "about": {"@id": AUTOR_ID},
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(cats),
            "itemListElement": [
                {"@type": "ListItem", "position": i, "name": nome,
                 "item": {"@id": f"{BASE}/categoria/{slug}/#page"}}
                for i, (slug, nome, _) in enumerate(cats, start=1)
            ],
        },
    },
    breadcrumb([("Início", BASE + "/"), ("Categorias", BASE + "/categoria/")]),
]
injetar(p, grafo)
relatorio.append(("categoria/ (hub)", len(cats)))

# ---------------------------------------------------------------- /arquetipos/
p = RAIZ / "arquetipos" / "index.html"
h, meta = ler(p)
# Os h3 da pagina sao os arquetipos, ate o bloco "E as trinta obras", que ja e
# rodape de navegacao e nao mais um arquetipo.
h3s = [texto(x) for x in re.findall(r"<h3[^>]*>(.*?)</h3>", h, re.S)]
arqs = []
for nome in h3s:
    if nome.lower().startswith("e as trinta"):
        break
    arqs.append(nome)
url = BASE + "/arquetipos/"
grafo = [
    {
        "@type": "CollectionPage",
        "@id": url + "#page",
        "url": url,
        "name": "Arquétipos dos personagens de Domenico Falco",
        "description": meta["desc"],
        "inLanguage": "pt-BR",
        "isPartOf": {"@id": SITE_ID},
        "about": {"@id": AUTOR_ID},
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(arqs),
            "itemListElement": [
                {"@type": "ListItem", "position": i, "name": nome}
                for i, nome in enumerate(arqs, start=1)
            ],
        },
    },
    breadcrumb([("Início", BASE + "/"), ("Arquétipos", url)]),
]
injetar(p, grafo)
relatorio.append(("arquetipos/", len(arqs)))

for nome, n in relatorio:
    print(f"  {nome:34s} {n:2d} itens no ItemList")
print(f"\nIds de obra conferidos contra a home: {len(IDS_HOME)} validos")
if orfas:
    print(f"ATENCAO, ids que a home nao tem: {orfas}")
else:
    print("Nenhum id orfao: todo livro citado nas categorias existe na home.")
if "--dry-run" in sys.argv:
    print("\n(dry-run, nada escrito)")
