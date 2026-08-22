# -*- coding: utf-8 -*-
"""
Adiciona o credito "Produzido por FalcoStrategy.com.br" no rodape de todas as
paginas do site.

O site nao tem layout compartilhado unico (so o blog herda de _includes/base.njk),
entao chrome de rodape vive duplicado em 13 arquivos, em 4 formatos diferentes:
  1. paginas com <p class="credit">        -> insere logo abaixo
  2. _includes/base.njk, com <p style=...> -> insere logo abaixo
  3. categoria/ e newsletter/, sem credito -> insere depois do paragrafo da marca
  4. LPs (audiolivro), rodape de uma linha  -> insere antes de </footer>

Idempotente: arquivo que ja tem o link e pulado.
Uso: python .claude/rodape_falco_strategy.py [--dry-run]
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
LINK = ('<p class="credit" style="font-size:12px;">Produzido por '
        '<a href="https://falcostrategy.com.br" target="_blank" rel="noopener" '
        'style="color:var(--gold-bright,#e6c467);text-decoration:underline;text-underline-offset:2px;">'
        'FalcoStrategy.com.br</a></p>')

ANCORAS = [
    (r'<p class="credit">.*?</p>', "depois do credito de capas"),
    (r'<p style="font-size:12px;">Arte das capas.*?</p>', "depois do credito (base.njk)"),
    (r'<p>Ficção histórica que entrelaça.*?</p>', "depois do paragrafo da marca"),
]

alvos = sorted(
    p for p in RAIZ.rglob("*")
    if p.suffix in (".html", ".njk")
    and "node_modules" not in p.parts and "_site" not in p.parts
    and "<footer" in p.read_text(encoding="utf-8", errors="ignore")
)

feitos, pulados = [], []
for arq in alvos:
    html = arq.read_text(encoding="utf-8")
    rel = arq.relative_to(RAIZ).as_posix()
    if "falcostrategy.com.br" in html.lower():
        pulados.append((rel, "ja tinha"))
        continue

    novo = None
    for padrao, motivo in ANCORAS:
        m = re.search(padrao, html, re.S)
        if not m:
            continue
        # Preserva a indentacao da linha ancorada.
        inicio_linha = html.rfind("\n", 0, m.start()) + 1
        indent = re.match(r"[ \t]*", html[inicio_linha:m.start()]).group(0)
        novo = html[:m.end()] + "\n" + indent + LINK + html[m.end():]
        onde = motivo
        break

    if novo is None:
        m = re.search(r"</footer>", html)
        if not m:
            pulados.append((rel, "SEM ancora e sem </footer>"))
            continue
        inicio_linha = html.rfind("\n", 0, m.start()) + 1
        indent = re.match(r"[ \t]*", html[inicio_linha:m.start()]).group(0)
        novo = html[:m.start()] + LINK + "\n" + indent + html[m.start():]
        onde = "antes de </footer>"

    if "--dry-run" not in sys.argv:
        arq.write_text(novo, encoding="utf-8")
    feitos.append((rel, onde))

print(f"Arquivos com rodape: {len(alvos)}")
for rel, onde in feitos:
    print(f"  OK    {rel:52s} {onde}")
for rel, motivo in pulados:
    print(f"  PULOU {rel:52s} {motivo}")
if "--dry-run" in sys.argv:
    print("\n(dry-run, nada escrito)")
