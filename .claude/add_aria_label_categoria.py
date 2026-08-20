"""
Lote 3, continuacao: mesmo fix do index.html (aria-label distinto em cada
"Comprar na Amazon"), agora nas 5 paginas de categoria que tem grade de livros.
Usa o <h3> mais recente visto antes de cada link.

Script de uso unico, mantido so por rastreabilidade.
"""
import re

ROOT = r"C:\Users\falco\OneDrive\BackUp\2. Carreira\1. JF Design\Projetos\Livros Dô\Site\livrosdofalco"

FILES = [
    r"categoria\submundo-traicoes-misterios\index.html",
    r"categoria\raizes-sacrificio-familia\index.html",
    r"categoria\mulheres-donas-do-seu-destino\index.html",
    r"categoria\fe-misticismo-desconhecido\index.html",
    r"categoria\jornadas-epicas-sobrevivencia\index.html",
]

h3_re = re.compile(r"<h3>(.*?)</h3>")
link_re = re.compile(r'(<a class="btn small( solid)?" href="[^"]+")(\s+target="_blank" rel="noopener">)Comprar na Amazon(</a>)')

total = 0
for rel in FILES:
    path = ROOT + "\\" + rel
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    last_h3 = None
    changed = 0
    for i, line in enumerate(lines):
        m = h3_re.search(line)
        if m:
            last_h3 = m.group(1).replace("&amp;", "&").replace("&middot;", "\u00b7")

        if "aria-label=" in line:
            continue

        m2 = link_re.search(line)
        if m2:
            label = f"Comprar {last_h3} na Amazon" if last_h3 else "Comprar na Amazon"
            new_line = line[: m2.start(1)] + m2.group(1) + f' aria-label="{label}"' + m2.group(3) + "Comprar na Amazon" + m2.group(4) + line[m2.end():]
            lines[i] = new_line
            changed += 1

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"{rel}: {changed} link(s) alterado(s)")
    total += changed

print(f"Total: {total}")
