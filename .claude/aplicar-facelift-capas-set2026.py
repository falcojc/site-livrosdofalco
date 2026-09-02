"""
Aplica as 6 capas com facelift (ja publicadas no KDP em 02/09/2026) nos arquivos
covers/*.jpg e covers/*.webp do site. Fonte: 1696x2528 (padrao de exportacao do
KDP), redimensionada para largura 400 (mesma convencao ja usada nas outras
capas do catalogo) e comprimida. O .book-cover do site tem aspect-ratio
733/1100 com object-fit:cover, entao a leve diferenca de proporcao (0,671 vs
0,667) e absorvida no recorte automatico do navegador, sem precisar cortar
manualmente.

Nao mexe em HTML: os <img> de capa nao tem width/height fixo (so
loading="lazy"), entao trocar o arquivo no mesmo caminho basta.

Uso: python .claude/aplicar-facelift-capas-set2026.py
"""
from pathlib import Path
from PIL import Image

SITE_ROOT = Path(__file__).resolve().parent.parent
OBRAS_ROOT = SITE_ROOT.parent.parent / "2. Produto" / "Catalogo" / "Obras Literárias"

TARGET_W = 400
JPG_QUALITY = 85
WEBP_QUALITY = 68

# (pasta da obra, arquivo facelift escolhido, slug no site)
ITENS = [
    ("19. O Asilo/2. Capa", "Facelift - O Asilo 2026.jpg", "o-asilo"),
    ("8. Mariana & José Inácio/2. Capa", "Facelift Capa Mariana e José Inácio 2026 v2.jpg", "mariana-e-jose-inacio"),
    ("23. Destinos Cruzados/2. Capa", "Facelift - Capa - Destinos Cruzados parte 1 v2.jpg", "destinos-cruzados"),
    ("25. O que eu lembro deles/2. Capa", "Facelift - Nova Capa - O que eu lembro deles - 2026.jpg", "o-que-eu-lembro-deles"),
    ("6. Os Italianos/2. eBook", "Facelift - Capa - Os Italianos -v1.jpg", "os-italianos"),
    ("4. Julius/2. Capa", "Facelift - New Cover Julius 2026.jpg", "julius"),
]


def processar(pasta, arquivo, slug):
    origem = OBRAS_ROOT / pasta / arquivo
    img = Image.open(origem).convert("RGB")
    w, h = img.size
    new_h = round(h * TARGET_W / w)
    resized = img.resize((TARGET_W, new_h), Image.LANCZOS)

    jpg_out = SITE_ROOT / "covers" / f"{slug}.jpg"
    webp_out = SITE_ROOT / "covers" / f"{slug}.webp"

    antes_jpg = jpg_out.stat().st_size if jpg_out.exists() else 0
    antes_webp = webp_out.stat().st_size if webp_out.exists() else 0

    resized.save(jpg_out, "JPEG", quality=JPG_QUALITY, optimize=True)
    resized.save(webp_out, "WEBP", quality=WEBP_QUALITY, method=6)

    depois_jpg = jpg_out.stat().st_size
    depois_webp = webp_out.stat().st_size

    print(f"{slug:24s} {img.size} -> {resized.size}")
    print(f"  jpg : {antes_jpg/1024:7.1f} KiB -> {depois_jpg/1024:7.1f} KiB")
    print(f"  webp: {antes_webp/1024:7.1f} KiB -> {depois_webp/1024:7.1f} KiB")


def main():
    for pasta, arquivo, slug in ITENS:
        processar(pasta, arquivo, slug)


if __name__ == "__main__":
    main()
