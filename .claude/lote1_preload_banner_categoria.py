"""
Complementa a propagacao do Lote 1: preload da imagem do hero de cada
pagina de categoria (mesmo padrao do index.html, que ja preloada o banner
do carrossel). O <img fetchpriority="high"> ja existia, so faltava o hint
no <head>.

Script de uso unico, mantido so por rastreabilidade.
"""
ROOT = r"C:\Users\falco\OneDrive\BackUp\2. Carreira\1. JF Design\Projetos\Livros Dô\Site\livrosdofalco"

PAGES = [
    "submundo-traicoes-misterios",
    "raizes-sacrificio-familia",
    "mulheres-donas-do-seu-destino",
    "fe-misticismo-desconhecido",
    "jornadas-epicas-sobrevivencia",
]

ANCHOR = '<link rel="preload" as="font" type="font/woff2" href="/fonts/cinzel-63551c.woff2" crossorigin>'

for slug in PAGES:
    path = ROOT + "\\categoria\\" + slug + "\\index.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    preload_img = f'<link rel="preload" as="image" fetchpriority="high" href="/categoria/{slug}/banner.jpg">'
    if ANCHOR not in content:
        print(f"{slug}: ANCORA NAO ACHADA")
        continue
    if preload_img in content:
        print(f"{slug}: ja tinha, pulado")
        continue

    content = content.replace(ANCHOR, ANCHOR + "\n" + preload_img, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{slug}: preload do banner inserido")
