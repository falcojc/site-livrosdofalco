# -*- coding: utf-8 -*-
"""
Reordena os 26 book-card de #obras-unicas na Home, na ordem pedida pelo
Falco em 03/09/2026 (destacar as capas com facelift, agrupar por tema).
Mantem os 8 primeiros visiveis (sem book-card--hidden) e os demais 18
ocultos atras do "Ver mais", igual a convencao atual. Atualiza tambem os
3 thumbnails de preview (.obras-ver-mais-peek) para os 3 primeiros ocultos.

Usa um parser de divs aninhados (conta <div> abertas/fechadas) em vez de
regex por linha em branco, pra nao depender do espacamento exato do
arquivo e nao cortar o ultimo bloco errado.

Le e escreve com newline='' para nao converter LF -> CRLF (arquivo e 100% LF).

Uso: python .claude/reorganizar-home-obras-unicas-set2026.py [--dry-run]
"""
import re
import sys
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent
INDEX = SITE_ROOT / "index.html"

NOVA_ORDEM = [
    # 1a fileira - mantida
    "o-comandante", "o-siciliano", "um-lugar-ao-sol", "a-vila",
    # 2a fileira
    "amor-e-odio", "os-dois-irmaos", "os-italianos", "os-refugiados",
    # 3a fileira
    "o-asilo", "o-que-eu-lembro-deles", "a-viagem", "mariana-e-jose-inacio",
    # 4a fileira
    "julius", "o-jesuita", "os-templarios", "sangue-frio",
    # 5a fileira
    "o-tesouro-maldito", "mestre-das-tormentas", "o-marciano", "o-reino",
    # 6a fileira
    "joana", "a-industria-do-vicio", "reflexoes-sobre-a-vida", "a-teia",
    # 7a fileira
    "akira", "a-casa-dos-prazeres",
]
N_VISIVEIS = 8

INICIO = '<div class="books-grid" id="obras-unicas">'
FIM = '<div class="obras-ver-mais-wrap">'

DIV_OPEN = re.compile(r"<div\b")
DIV_CLOSE = re.compile(r"</div>")


def bloco_div(texto, start):
    """Retorna o bloco '<div ...>...</div>' que comeca em start, respeitando
    divs aninhadas dentro dele."""
    fim_tag_abertura = texto.index(">", start) + 1
    depth = 1
    pos = fim_tag_abertura
    while depth > 0:
        m_open = DIV_OPEN.search(texto, pos)
        m_close = DIV_CLOSE.search(texto, pos)
        if not m_close:
            raise ValueError("div sem fechamento")
        if m_open and m_open.start() < m_close.start():
            depth += 1
            pos = m_open.end()
        else:
            depth -= 1
            pos = m_close.end()
    return texto[start:pos]


def main():
    texto = INDEX.read_text(encoding="utf-8")

    i0 = texto.index(INICIO) + len(INICIO)
    i1 = texto.index(FIM)
    miolo = texto[i0:i1]

    blocos = {}
    spans = []
    for m in re.finditer(r'<div class="book-card[^"]*" id="([^"]+)">', miolo):
        oid = m.group(1)
        b = bloco_div(miolo, m.start())
        blocos[oid] = b
        spans.append((m.start(), m.start() + len(b)))

    faltando = set(NOVA_ORDEM) - set(blocos)
    sobrando = set(blocos) - set(NOVA_ORDEM)
    if faltando or sobrando:
        raise SystemExit(f"Divergencia de ids. Faltando: {faltando} | Sobrando: {sobrando}")

    novos_blocos = []
    for idx, oid in enumerate(NOVA_ORDEM):
        bloco = blocos[oid]
        bloco = bloco.replace('class="book-card book-card--hidden"', 'class="book-card"')
        if idx >= N_VISIVEIS:
            bloco = bloco.replace('class="book-card"', 'class="book-card book-card--hidden"', 1)
        novos_blocos.append(bloco)

    # preserva exatamente o que vinha antes do 1o card e depois do
    # ultimo (inclui o </div> de fechamento do proprio .books-grid, cuja
    # abertura foi cortada junto com o marcador INICIO) e o separador
    # entre cards, tudo medido no arquivo original - nao hardcoded.
    spans.sort()
    cabeca = miolo[:spans[0][0]]
    cauda = miolo[spans[-1][1]:]
    separador = miolo[spans[0][1]:spans[1][0]]

    novo_miolo = cabeca + separador.join(novos_blocos) + cauda
    texto = texto[:i0] + novo_miolo + texto[i1:]

    # --- atualiza os 3 thumbnails de preview (primeiros 3 ocultos na nova ordem)
    titulos = {}
    for oid in NOVA_ORDEM:
        t = re.search(r"<h3>(.*?)</h3>", blocos[oid], re.S)
        titulos[oid] = re.sub(r"&amp;", "&", t.group(1)) if t else oid

    peek_ids = NOVA_ORDEM[N_VISIVEIS:N_VISIVEIS + 3]
    peek_html = "\n".join(
        f'        <a href="#{oid}" class="obras-ver-mais-peek-item" title="{titulos[oid]}">'
        f'<img src="covers/{oid}.webp" alt="" loading="lazy"></a>'
        for oid in peek_ids
    )
    texto = re.sub(
        r'(<div class="obras-ver-mais-peek">\n).*?(\n\s*</div>\n\s*<button type="button" id="obras-ver-mais")',
        lambda m: m.group(1) + peek_html + m.group(2),
        texto, count=1, flags=re.S,
    )

    if "--dry-run" in sys.argv:
        print(f"[dry-run] {len(novos_blocos)} cards reordenados, {N_VISIVEIS} visiveis.")
        print("Peek novo:", peek_ids)
        return

    with open(INDEX, "w", encoding="utf-8", newline="") as f:
        f.write(texto)
    print(f"OK: {len(novos_blocos)} cards reordenados, {N_VISIVEIS} visiveis, peek = {peek_ids}")


if __name__ == "__main__":
    main()
