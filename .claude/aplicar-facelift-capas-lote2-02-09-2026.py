"""
Aplica as 6 capas com facelift do lote 2 (Os Templarios, O Jesuita, O Mestre das
Tormentas, Sangue Frio, O Tesouro Maldito, O Marciano) nos arquivos covers/*.jpg
e covers/*.webp do site. Mesma logica do lote 1
(aplicar-facelift-capas-set2026.py): fonte redimensionada para largura 400,
comprimida, sem mexer em HTML (os <img> de capa nao tem width/height fixo).

Uso: python .claude/aplicar-facelift-capas-lote2-02-09-2026.py
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
    ("3. Os Templários/2. eBook", "Facelift Capa Os templarios 2026.jpg", "os-templarios"),
    ("5. O Jesuita/2. eBook", "facelift - capa O jesuíta 2026.jpg", "o-jesuita"),
    ("2. John Storm/2. eBook/Capa", "Gemini_Generated_Image_7rgei07rgei07rge.jpg", "mestre-das-tormentas"),
    ("10. Sangue Frio/2. eBook", "Facelift - Sangue Frio 2026.jpg", "sangue-frio"),
    ("14. O Tesouro Maldito/2. eBook", "Facelift - Tesouro maldito 2026.jpg", "o-tesouro-maldito"),
    ("1. O Marciano/2. Capa", "Facelift Capa - O Marciano 2026 v2.jpg", "o-marciano"),
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
