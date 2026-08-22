# -*- coding: utf-8 -*-
"""
Sincroniza e enriquece o JSON-LD da home para leitura por maquina
(LLM, AI Overview, Rufus da Amazon).

O que faz, e por que cada coisa:
  1. SINCRONIZA: todo card de obra na home vira um no Book. Antes, obra nova
     entrava no card e nunca no dado estruturado (foi o caso de O Comandante).
  2. Da um @id estavel ao Person e faz os Books apontarem para ele, em vez de
     repetir o objeto autor 30 vezes. Sem isso sao 30 homonimos soltos; com
     isso e uma entidade so, que e como maquina reconhece autor.
  3. Adiciona `image` (a capa) e `keywords` (a tag do card) em cada Book.
  4. Adiciona `identifier` com o ASIN e `sameAs`/`offers.url` com a URL LIMPA
     da Amazon, sem a tag de afiliado: link de afiliado nao entra em dado
     estruturado. O clique do usuario continua indo pelo link visivel do card.
  5. Adiciona Instagram e TikTok no sameAs do autor.

Idempotente. Rodar de novo depois de publicar obra nova mantem tudo em dia.
Uso: python .claude/enriquecer_jsonld_ia.py [--dry-run]
"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
INDEX = RAIZ / "index.html"
BASE = "https://www.livrosdofalco.com.br"
AUTOR_ID = BASE + "/#domenico-falco"

html = INDEX.read_text(encoding="utf-8")

# --- 1. Ler os cards da home ------------------------------------------------
cards = {}
for m in re.finditer(
    r'<div class="book-card[^"]*" id="([^"]+)">(.*?)(?=<div class="book-card|</section>)',
    html, re.S):
    slug, corpo = m.group(1), m.group(2)
    img = re.search(r'<img src="([^"]+)"', corpo)
    asin = re.search(r'amazon\.com\.br/dp/([A-Z0-9]{10})', corpo)
    h3 = re.search(r'<h3>(.*?)</h3>', corpo, re.S)
    tag = re.search(r'<div class="book-tag">(.*?)</div>', corpo, re.S)
    desc = re.search(r'<h3>.*?</h3>\s*<p>(.*?)</p>', corpo, re.S)
    cards[slug] = {
        "slug": slug,
        "titulo": h3.group(1).strip() if h3 else None,
        "image": BASE + "/" + img.group(1).lstrip("/") if img else None,
        "asin": asin.group(1) if asin else None,
        "tag": tag.group(1).strip() if tag else None,
        "desc": re.sub(r"\s+", " ", desc.group(1)).strip() if desc else None,
    }

# --- 2. Isolar e parsear o bloco JSON-LD ------------------------------------
bloco = re.search(
    r'(<script type="application/ld\+json">\s*)(\{.*?\})(\s*</script>)', html, re.S)
if not bloco:
    sys.exit("ERRO: bloco JSON-LD nao encontrado no index.html")
dados = json.loads(bloco.group(2))
grafo = dados["@graph"]

# --- 3. Person --------------------------------------------------------------
REDES = ["https://www.instagram.com/livrosdofalco/",
         "https://www.tiktok.com/@livros_dofalco"]
autor = next((n for n in grafo if n.get("@type") == "Person"
              and n.get("name") == "Domenico Falco" and "jobTitle" in n), None)
if autor is None:
    sys.exit("ERRO: no Person do autor nao encontrado")
autor["@id"] = AUTOR_ID
autor["sameAs"] = autor.get("sameAs", []) + [r for r in REDES
                                             if r not in autor.get("sameAs", [])]

# --- 4. Casar Book <-> card (por fragmento de url, senao por titulo) --------
livros = [n for n in grafo if n.get("@type") == "Book"]
por_titulo = {c["titulo"]: c for c in cards.values() if c["titulo"]}
usados = set()

def enriquecer(no, card):
    no["@id"] = no.get("url") or (BASE + "/#" + card["slug"])
    no["author"] = {"@id": AUTOR_ID}
    if card["image"]:
        no["image"] = card["image"]
    if card["tag"]:
        no["keywords"] = card["tag"]
    if card["asin"]:
        limpa = "https://www.amazon.com.br/dp/" + card["asin"]
        no["identifier"] = {"@type": "PropertyValue", "propertyID": "ASIN",
                            "value": card["asin"]}
        no["sameAs"] = limpa
        no["offers"] = {"@type": "Offer", "url": limpa,
                        "availability": "https://schema.org/InStock",
                        "seller": {"@type": "Organization", "name": "Amazon"}}

for no in livros:
    frag = no.get("url", "").split("#")[-1]
    card = cards.get(frag) or por_titulo.get(no.get("name"))
    if card:
        usados.add(card["slug"])
        enriquecer(no, card)
    else:
        print(f"AVISO: Book sem card correspondente: {no.get('name')!r}")

# --- 5. Criar os Books que faltam (card sem no) -----------------------------
criados = []
ultimo = max(i for i, n in enumerate(grafo) if n.get("@type") == "Book")
for card in cards.values():
    if card["slug"] in usados or not card["titulo"]:
        continue
    novo = {"@type": "Book", "name": card["titulo"],
            "author": {"@id": AUTOR_ID}, "genre": "Ficção Histórica",
            "description": card["desc"] or "",
            "url": BASE + "/#" + card["slug"], "inLanguage": "pt-BR"}
    enriquecer(novo, card)
    ultimo += 1
    grafo.insert(ultimo, novo)
    criados.append(card["titulo"])

# --- 6. Reescrever ----------------------------------------------------------
novo_json = json.dumps(dados, ensure_ascii=False, indent=2)
saida = html[:bloco.start(2)] + novo_json + html[bloco.end(2):]
livros = [n for n in grafo if n.get("@type") == "Book"]

print(f"Cards na home       : {len(cards)}")
print(f"Books no JSON-LD    : {len(livros)}")
print(f"Books criados agora : {criados if criados else 'nenhum'}")
print(f"Com capa            : {sum(1 for n in livros if n.get('image'))}")
print(f"Com ASIN/oferta     : {sum(1 for n in livros if n.get('offers'))}")
print(f"Com keywords        : {sum(1 for n in livros if n.get('keywords'))}")

if "--dry-run" in sys.argv:
    print("\n(dry-run, nada escrito)")
else:
    INDEX.write_text(saida, encoding="utf-8")
    print("\nindex.html reescrito.")
