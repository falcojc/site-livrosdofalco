"""
Lote 3 (acessibilidade): adiciona aria-label distinto em cada link "Comprar na Amazon".
O Lighthouse reprova links com o mesmo nome acessivel apontando pra destinos diferentes.
Usa o <h3> mais recente visto antes de cada link pra montar o aria-label.
Script de uso unico, mantido aqui so por rastreabilidade.
"""
import re

path = r"C:\Users\falco\OneDrive\BackUp\2. Carreira\1. JF Design\Projetos\Livros Dô\Site\livrosdofalco\index.html"

with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

last_h3 = None
h3_re = re.compile(r"<h3>(.*?)</h3>")
link_re = re.compile(r'(<a class="btn small( solid)?" href="[^"]+")(\s+target="_blank" rel="noopener">)Comprar na Amazon(</a>)')

changed = 0
for i, line in enumerate(lines):
    m = h3_re.search(line)
    if m:
        # remove html entities simples e tags aninhadas (ex: &amp;)
        title = m.group(1).replace("&amp;", "&")
        last_h3 = title

    m2 = link_re.search(line)
    if m2:
        if "ascsubtag=home-catalogo" in line:
            label = "Ver cat\u00e1logo completo na Amazon"
        elif last_h3:
            label = f"Comprar {last_h3} na Amazon"
        else:
            label = "Comprar na Amazon"
        # insere aria-label antes de target=
        new_line = line[: m2.start(1)] + m2.group(1) + f' aria-label="{label}"' + m2.group(3) + "Comprar na Amazon" + m2.group(4) + line[m2.end():]
        lines[i] = new_line
        changed += 1

with open(path, "w", encoding="utf-8") as f:
    f.writelines(lines)

print(f"Links alterados: {changed}")
