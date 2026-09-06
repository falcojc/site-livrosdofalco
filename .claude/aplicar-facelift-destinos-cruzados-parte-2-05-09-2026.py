"""
Aplica a nova capa (facelift v3, com tipografia ja embutida na arte, no mesmo
padrao serifado do irmao "Destinos Cruzados: Parte 1") em Destinos Cruzados:
Parte 2. Diferente dos lotes de 02-03/09, esta arte ja chega com titulo e
autor prontos: nao passa pelo compositor de tipografia (.claude/tipografia/
compor_capa.py), que serve para arte SEM texto.

Toca dois destinos, ambos derivados da mesma fonte:
  1. .claude/epub/capas/destinos-cruzados-parte-2.jpg
     fonte canonica usada pelo motor de EPUB (--cover) e pelo gerador de capa
     de PDP (.claude/pdp/gerar_capas.py). Redimensionada para a mesma largura
     dos irmaos da serie (~1060px), para nao destoar em peso de arquivo.
  2. Site/livrosdofalco/covers/destinos-cruzados-parte-2.{jpg,webp}
     miniatura de card do site (400px), mesma convencao dos lotes anteriores:
     jpg q85, webp q68, sem mexer em HTML.

Uso: python .claude/aplicar-facelift-destinos-cruzados-parte-2-05-09-2026.py
"""
from pathlib import Path
from PIL import Image

SITE_ROOT = Path(__file__).resolve().parent.parent
RAIZ = SITE_ROOT.parent.parent
ORIGEM = (RAIZ / "2. Produto" / "Catalogo" / "Obras Literárias"
          / "24. Destinos Cruzados Parte 2" / "2. eBook"
          / "Facelift Nova Capa - Destinos Cruzados Parte II v3.jpg")
SLUG = "destinos-cruzados-parte-2"

LARGURA_EPUB = 1060   # media dos irmaos da serie em .claude/epub/capas
QUALIDADE_EPUB = 90
LARGURA_SITE = 400
JPG_QUALITY = 85
WEBP_QUALITY = 68


def redimensiona(img: Image.Image, largura: int) -> Image.Image:
    altura = round(img.height * largura / img.width)
    return img.resize((largura, altura), Image.LANCZOS)


def main():
    if not ORIGEM.is_file():
        raise SystemExit(f"arte nao encontrada: {ORIGEM}")

    original = Image.open(ORIGEM).convert("RGB")
    print(f"origem: {original.size}, {ORIGEM.stat().st_size / 1024:.0f} KiB")

    # 1) fonte canonica do motor de EPUB / gerador de capa de PDP
    destino_epub = RAIZ / ".claude" / "epub" / "capas" / f"{SLUG}.jpg"
    antes = destino_epub.stat().st_size if destino_epub.exists() else 0
    epub_img = redimensiona(original, LARGURA_EPUB)
    epub_img.save(destino_epub, "JPEG", quality=QUALIDADE_EPUB, optimize=True, progressive=True)
    print(f"epub/capas: {epub_img.size}  {antes/1024:.0f} KiB -> {destino_epub.stat().st_size/1024:.0f} KiB")

    # 2) miniatura de card do site
    site_img = redimensiona(original, LARGURA_SITE)
    jpg_out = SITE_ROOT / "covers" / f"{SLUG}.jpg"
    webp_out = SITE_ROOT / "covers" / f"{SLUG}.webp"
    antes_jpg = jpg_out.stat().st_size if jpg_out.exists() else 0
    antes_webp = webp_out.stat().st_size if webp_out.exists() else 0
    site_img.save(jpg_out, "JPEG", quality=JPG_QUALITY, optimize=True)
    site_img.save(webp_out, "WEBP", quality=WEBP_QUALITY, method=6)
    print(f"covers: {site_img.size}")
    print(f"  jpg : {antes_jpg/1024:7.1f} KiB -> {jpg_out.stat().st_size/1024:7.1f} KiB")
    print(f"  webp: {antes_webp/1024:7.1f} KiB -> {webp_out.stat().st_size/1024:7.1f} KiB")


if __name__ == "__main__":
    main()
