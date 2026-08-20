"""
Lote 3, continuacao: insere <main> logo apos </header> e fecha logo antes de
<footer>, nos arquivos estaticos que faltavam (categoria/* e a PDP). O
index.html e o base.njk ja foram tratados a parte.

Script de uso unico, mantido so por rastreabilidade.
"""
ROOT = r"C:\Users\falco\OneDrive\BackUp\2. Carreira\1. JF Design\Projetos\Livros Dô\Site\livrosdofalco"

FILES = [
    r"categoria\index.html",
    r"categoria\submundo-traicoes-misterios\index.html",
    r"categoria\raizes-sacrificio-familia\index.html",
    r"categoria\mulheres-donas-do-seu-destino\index.html",
    r"categoria\fe-misticismo-desconhecido\index.html",
    r"categoria\jornadas-epicas-sobrevivencia\index.html",
    r"o-mestre-das-tormentas\index.html",
]

for rel in FILES:
    path = ROOT + "\\" + rel
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    header_idx = None
    footer_idx = None
    for i, line in enumerate(lines):
        if line.strip() == "</header>" and header_idx is None:
            header_idx = i
        if line.strip() == "<footer>":
            footer_idx = i
            break

    if header_idx is None or footer_idx is None or footer_idx <= header_idx:
        print(f"{rel}: PULADO, nao achei </header> ou <footer> no formato esperado (header={header_idx}, footer={footer_idx})")
        continue

    # insere </main> antes do footer primeiro (indice maior, nao desloca o header_idx)
    lines.insert(footer_idx, "</main>\n\n")
    lines.insert(header_idx + 1, "\n<main>\n")

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"{rel}: <main> inserido (header linha {header_idx+1}, footer original linha {footer_idx+1})")
