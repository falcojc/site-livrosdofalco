"""
Lote 3, continuacao: propaga os fixes de acessibilidade que so tinham ido pra
index.html (home) pro resto do site: categoria/*, o-mestre-das-tormentas (PDP)
e _includes/base.njk (blog + posts).

1. Contraste: #6f6552 -> #8a7f68 em todo arquivo da lista.
2. hero-dot: CSS de 8x8 -> 24x24 real (mesmo bloco aplicado no index.html) no base.njk.

<main> e a checagem de headings sao feitas a parte, via Edit, porque a estrutura
de cada arquivo (onde fica o </header> e o <footer>) nao e identica.

Script de uso unico, mantido so por rastreabilidade.
"""
import re

ROOT = r"C:\Users\falco\OneDrive\BackUp\2. Carreira\1. JF Design\Projetos\Livros Dô\Site\livrosdofalco"

FILES_CONTRASTE = [
    r"_includes\base.njk",
    r"categoria\index.html",
    r"categoria\submundo-traicoes-misterios\index.html",
    r"categoria\raizes-sacrificio-familia\index.html",
    r"categoria\mulheres-donas-do-seu-destino\index.html",
    r"categoria\fe-misticismo-desconhecido\index.html",
    r"categoria\jornadas-epicas-sobrevivencia\index.html",
    r"o-mestre-das-tormentas\index.html",
]

changed = 0
for rel in FILES_CONTRASTE:
    path = ROOT + "\\" + rel
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    n = content.count("#6f6552")
    content = content.replace("#6f6552", "#8a7f68")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    changed += n
    print(f"{rel}: {n} ocorrencia(s) trocada(s)")

print(f"Total contraste: {changed}")

# hero-dot no base.njk: mesmo bloco aplicado no index.html
base_path = ROOT + r"\_includes\base.njk"
with open(base_path, "r", encoding="utf-8") as f:
    base = f.read()

old_block = """  .hero-dots{position:absolute;bottom:18px;right:20px;display:flex;gap:8px;z-index:2;}
  .hero-dot{width:8px;height:8px;border-radius:50%;border:1px solid var(--gold);background:transparent;padding:0;cursor:pointer;}
  .hero-dot.is-active{background:var(--gold);}"""

new_block = """  .hero-dots{position:absolute;bottom:10px;right:12px;display:flex;gap:2px;z-index:2;}
  .hero-dot{width:24px;height:24px;border:0;background:transparent;padding:0;cursor:pointer;display:flex;align-items:center;justify-content:center;}
  .hero-dot::before{content:"";width:8px;height:8px;border-radius:50%;border:1px solid var(--gold);background:transparent;}
  .hero-dot.is-active{background:transparent;}
  .hero-dot.is-active::before{background:var(--gold);}"""

if old_block in base:
    base = base.replace(old_block, new_block)
    with open(base_path, "w", encoding="utf-8") as f:
        f.write(base)
    print("base.njk: hero-dot atualizado pra 24x24")
else:
    print("base.njk: bloco hero-dot NAO encontrado como esperado, checar manualmente")
