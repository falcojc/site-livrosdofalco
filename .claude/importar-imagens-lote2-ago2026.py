"""
Segundo lote de posts (ago/2026): Um Lugar ao Sol, Amor e Odio, A Viagem,
O Que Eu Lembro Deles, Os Refugiados. Mesma receita do lote 1
(importar-imagens-lote-ago2026.py): JPG 1600px pro corpo/fonte da capa,
WEBP 1200px/qualidade 80 so pra capa.

Uso: python .claude/importar-imagens-lote2-ago2026.py
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = Path(r"C:\Users\falco\OneDrive\BackUp\2. Carreira\1. JF Design\Projetos\Livros Dô\2. Produto\Catalogo\Obras Literárias")

JPG_MAX_W = 1600
JPG_QUALITY = 88
WEBP_MAX_W = 1200
WEBP_QUALITY = 80

POSTS = [
    ("nova-york-anos-60-contracultura-woodstock-direitos-civis", [
        ("28. Um Lugar ao Sol/7. Blog/Post 1 - A Geração que Quebrou as Regras/O Festival de Woodstock (A Utopia de 1969).jpg", "capa-festival-woodstock.jpg", True),
        ("28. Um Lugar ao Sol/7. Blog/Post 1 - A Geração que Quebrou as Regras/Aula de Cênicas no Central Park.jpg", "aula-cenicas-central-park.jpg", False),
        ("28. Um Lugar ao Sol/7. Blog/Post 1 - A Geração que Quebrou as Regras/Malcom no Harlem (A Busca por Identidade).jpg", "malcom-harlem-identidade.jpg", False),
    ]),
    ("guerra-civil-espanhola-andaluzia-poder-traicao", [
        ("21. Amor e Ódio/7. Blog/Post 1/O Cerco de Málaga (O Resgate de Javier).jpg", "capa-cerco-malaga-resgate.jpg", True),
        ("21. Amor e Ódio/7. Blog/Post 1/As Oliveiras de Águas Calmas (A Juventude Antes da Guerra).jpg", "oliveiras-aguas-calmas-juventude.jpg", False),
        ("21. Amor e Ódio/7. Blog/Post 1/O Romance Clandestino (Paco e Carmen sob a Tempestade).jpg", "romance-clandestino-paco-carmen.jpg", False),
    ]),
    ("psicologia-confinamento-resgate-mar-mediterraneo-iate", [
        ("20. A Viagem/7. Blog/Post 1/O Iate Aurora no Mediterrâneo (O Luxo Inicial).jpg", "capa-iate-aurora-mediterraneo.jpg", True),
        ("20. A Viagem/7. Blog/Post 1/O Desgaste das Máscaras (Emília e Miguel).jpg", "desgaste-mascaras-emilia-miguel.jpg", False),
        ("20. A Viagem/7. Blog/Post 1/O Resgate à Deriva (O Ponto de Não Retorno).jpg", "resgate-deriva-ponto-nao-retorno.jpg", False),
    ]),
    ("blitz-belfast-conflito-irlanda-do-norte-the-troubles", [
        ("25. O que eu lembro deles/7. Blog/Post 1 - As Ruas de Belfast/O Conflito de Aidan (As Ruas de Belfast nos Anos 60) v2.jpg", "capa-ruas-belfast-conflito.jpg", True),
        ("25. O que eu lembro deles/7. Blog/Post 1 - As Ruas de Belfast/O Abrigo no Blitz de 1941 (O Nascimento do Amor).jpg", "abrigo-blitz-1941-belfast.jpg", False),
        ("25. O que eu lembro deles/7. Blog/Post 1 - As Ruas de Belfast/Killian e as Memórias na Varanda (O Presente Silencioso).jpg", "killian-memorias-varanda.jpg", False),
    ]),
    ("guerra-siria-campo-refugiados-cruz-vermelha-familias-separadas", [
        ("26. Os Refugiados/7. Blog/Post 1/O Soco de Alepo (A Cor e a Vida Antes de 2011).jpg", "capa-soco-alepo-antes-guerra.jpg", True),
        ("26. Os Refugiados/7. Blog/Post 1/A Marcha dos Despossuídos (A Longa Jornada a Pé).jpg", "marcha-despossuidos-fronteira.jpg", False),
        ("26. Os Refugiados/7. Blog/Post 1/Alzira e a Cruz Vermelha (A Força do Amor de Mãe).jpg", "alzira-cruz-vermelha-busca.jpg", False),
    ]),
]


def resize_save_jpg(src: Path, dst: Path, max_w: int, quality: int):
    img = Image.open(src).convert("RGB")
    if img.width > max_w:
        new_h = round(img.height * max_w / img.width)
        img = img.resize((max_w, new_h), Image.LANCZOS)
    dst.parent.mkdir(parents=True, exist_ok=True)
    img.save(dst, "JPEG", quality=quality, optimize=True)
    return img.size


def resize_save_webp(src_jpg: Path, dst_webp: Path, max_w: int, quality: int):
    img = Image.open(src_jpg).convert("RGB")
    if img.width > max_w:
        new_h = round(img.height * max_w / img.width)
        img = img.resize((max_w, new_h), Image.LANCZOS)
    img.save(dst_webp, "WEBP", quality=quality, method=6)


def main():
    total_before = total_after = 0
    for slug, images in POSTS:
        dest_dir = ROOT / "blog" / "posts" / "media" / slug
        print(f"--- {slug} ---")
        for src_rel, dest_name, is_cover in images:
            src = SRC_ROOT / src_rel
            if not src.exists():
                print(f"  AVISO: nao encontrado: {src_rel}")
                continue
            before = src.stat().st_size
            dst_jpg = dest_dir / dest_name
            size = resize_save_jpg(src, dst_jpg, JPG_MAX_W, JPG_QUALITY)
            after = dst_jpg.stat().st_size
            total_before += before
            total_after += after
            print(f"  {dest_name:40s} {before/1024:7.0f}KB -> {after/1024:7.0f}KB  {size}")
            if is_cover:
                dst_webp = dst_jpg.with_suffix(".webp")
                resize_save_webp(dst_jpg, dst_webp, WEBP_MAX_W, WEBP_QUALITY)
                after_webp = dst_webp.stat().st_size
                print(f"  {dst_webp.name:40s}            -> {after_webp/1024:7.0f}KB (webp da capa)")
    print("-" * 60)
    print(f"TOTAL JPG: {total_before/1024:.0f}KB -> {total_after/1024:.0f}KB ({100*(1-total_after/total_before):.0f}% menor)")


if __name__ == "__main__":
    main()
