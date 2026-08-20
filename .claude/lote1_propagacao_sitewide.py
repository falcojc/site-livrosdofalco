"""
Fecha o gap do Lote 1: esse lote (defer no analytics.js, fontes locais com
preload) so tinha ido pro index.html, igual aconteceu com o Lote 3. Propaga
pros mesmos 8 arquivos que receberam o fix de acessibilidade.

Tres trocas, todas por string literal (o texto e identico em todo arquivo,
so a linha muda):

1. <script src="/analytics.js"></script> -> mesmo com defer
2. Bloco do Google Fonts remoto (preconnect + stylesheet) -> 2 links de
   preload das fontes locais
3. @font-face das 2 fontes (6 regras, mesmas do index.html) inserido logo
   depois do bloco :root{...}, que tem formatacao diferente por arquivo
   (por isso a busca e por linha, nao por string fixa)

Script de uso unico, mantido so por rastreabilidade.
"""
ROOT = r"C:\Users\falco\OneDrive\BackUp\2. Carreira\1. JF Design\Projetos\Livros Dô\Site\livrosdofalco"

FILES = [
    r"_includes\base.njk",
    r"categoria\index.html",
    r"categoria\submundo-traicoes-misterios\index.html",
    r"categoria\raizes-sacrificio-familia\index.html",
    r"categoria\mulheres-donas-do-seu-destino\index.html",
    r"categoria\fe-misticismo-desconhecido\index.html",
    r"categoria\jornadas-epicas-sobrevivencia\index.html",
    r"o-mestre-das-tormentas\index.html",
]

OLD_ANALYTICS = '<script src="/analytics.js"></script>'
NEW_ANALYTICS = '<script src="/analytics.js" defer></script>'

OLD_FONTS_HEAD = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700;900&family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">'
)
NEW_FONTS_HEAD = (
    '<link rel="preload" as="font" type="font/woff2" href="/fonts/eb-garamond-143e88.woff2" crossorigin>\n'
    '<link rel="preload" as="font" type="font/woff2" href="/fonts/cinzel-63551c.woff2" crossorigin>'
)

FONT_FACE_BLOCK = """  @font-face{font-family:'EB Garamond';font-style:normal;font-weight:400;font-display:swap;src:url('/fonts/eb-garamond-143e88.woff2') format('woff2');unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;}
  @font-face{font-family:'EB Garamond';font-style:normal;font-weight:500;font-display:swap;src:url('/fonts/eb-garamond-143e88.woff2') format('woff2');unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;}
  @font-face{font-family:'EB Garamond';font-style:normal;font-weight:600;font-display:swap;src:url('/fonts/eb-garamond-143e88.woff2') format('woff2');unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;}
  @font-face{font-family:'Cinzel';font-style:normal;font-weight:400;font-display:swap;src:url('/fonts/cinzel-63551c.woff2') format('woff2');unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;}
  @font-face{font-family:'Cinzel';font-style:normal;font-weight:600;font-display:swap;src:url('/fonts/cinzel-63551c.woff2') format('woff2');unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;}
  @font-face{font-family:'Cinzel';font-style:normal;font-weight:700;font-display:swap;src:url('/fonts/cinzel-63551c.woff2') format('woff2');unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;}
  @font-face{font-family:'Cinzel';font-style:normal;font-weight:900;font-display:swap;src:url('/fonts/cinzel-63551c.woff2') format('woff2');unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;}
"""

for rel in FILES:
    path = ROOT + "\\" + rel
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    report = []

    if OLD_ANALYTICS in content:
        content = content.replace(OLD_ANALYTICS, NEW_ANALYTICS, 1)
        report.append("defer ok")
    else:
        report.append("ANALYTICS NAO ACHADO")

    if OLD_FONTS_HEAD in content:
        content = content.replace(OLD_FONTS_HEAD, NEW_FONTS_HEAD, 1)
        report.append("preload fontes ok")
    else:
        report.append("BLOCO FONTS NAO ACHADO")

    lines = content.split("\n")
    root_idx = None
    close_idx = None
    for i, line in enumerate(lines):
        if line.strip() == ":root{":
            root_idx = i
            continue
        if root_idx is not None and line.strip() == "}":
            close_idx = i
            break

    if close_idx is not None:
        lines.insert(close_idx + 1, FONT_FACE_BLOCK.rstrip("\n"))
        content = "\n".join(lines)
        report.append("@font-face inserido")
    else:
        report.append("FECHAMENTO DE :root NAO ACHADO")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"{rel}: {', '.join(report)}")
