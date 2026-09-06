"""
Aplica a nova capa (facelift v2, tipografia serifada ja embutida na arte,
mesmo padrao da onda de 05/09) em A Industria do Vicio. A capa antiga usava
a fonte redonda com contorno branco da primeira geracao de artes do catalogo
(o mesmo estilo que Destinos Cruzados: Parte 2 tinha antes do facelift).

Toca os dois destinos derivados da mesma fonte:
  1. .claude/epub/capas/a-industria-do-vicio.jpg
     fonte canonica usada pelo motor de EPUB (--cover) e pelo gerador de capa
     de PDP (.claude/pdp/gerar_capas.py).
  2. Site/livrosdofalco/covers/a-industria-do-vicio.{jpg,webp}
     miniatura de card do site (400px): jpg q85, webp q68, sem mexer em HTML.

Uso: python .claude/aplicar-facelift-a-industria-do-vicio-05-09-2026.py
"""
from pathlib import Path
from PIL import Image

SITE_ROOT = Path(__file__).resolve().parent.parent
RAIZ = SITE_ROOT.parent.parent
ORIGEM = (RAIZ / "2. Produto" / "Catalogo" / "Obras Literárias"
          / "15. A indústria do vício" / "2. eBook"
          / "Facelift A Industria do Vicio v2.jpg")
SLUG = "a-industria-do-vicio"

LARGURA_EPUB = 1060
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

    destino_epub = RAIZ / ".claude" / "epub" / "capas" / f"{SLUG}.jpg"
    antes = destino_epub.stat().st_size if destino_epub.exists() else 0
    epub_img = redimensiona(original, LARGURA_EPUB)
    epub_img.save(destino_epub, "JPEG", quality=QUALIDADE_EPUB, optimize=True, progressive=True)
    print(f"epub/capas: {epub_img.size}  {antes/1024:.0f} KiB -> {destino_epub.stat().st_size/1024:.0f} KiB")

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
