# -*- coding: utf-8 -*-
"""
Gera covers/destinos-cruzados-fios-do-destino.jpg e .webp a partir da capa
final do omnibus (a mesma que foi para o KDP e esta embutida no EPUB
publicado - conferida por hash contra OEBPS/images/cover.jpg).

Mesma convencao dos scripts de facelift: largura 400px, jpg q85, webp q68.

Uso: python .claude/aplicar-capa-omnibus-destinos-cruzados-03-09-2026.py
"""
from pathlib import Path
from PIL import Image

SITE_ROOT = Path(__file__).resolve().parent.parent
ORIGEM = (SITE_ROOT.parent.parent / "2. Produto" / "Catalogo" / "Omnibus" /
          "Destinos Cruzados" / "3. capa" / "Capa Destinos Cruzados - v1 topo.jpg")
SLUG = "destinos-cruzados-fios-do-destino"

TARGET_W = 400
JPG_QUALITY = 85
WEBP_QUALITY = 68


def main():
    img = Image.open(ORIGEM).convert("RGB")
    w, h = img.size
    new_h = round(h * TARGET_W / w)
    resized = img.resize((TARGET_W, new_h), Image.LANCZOS)

    jpg_out = SITE_ROOT / "covers" / f"{SLUG}.jpg"
    webp_out = SITE_ROOT / "covers" / f"{SLUG}.webp"

    resized.save(jpg_out, "JPEG", quality=JPG_QUALITY, optimize=True)
    resized.save(webp_out, "WEBP", quality=WEBP_QUALITY, method=6)

    print(f"{SLUG}: {img.size} -> {resized.size}")
    print(f"  jpg : {jpg_out} ({jpg_out.stat().st_size/1024:.1f} KiB)")
    print(f"  webp: {webp_out} ({webp_out.stat().st_size/1024:.1f} KiB)")


if __name__ == "__main__":
    main()
