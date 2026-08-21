"""
Lote de posts novos (ago/2026): O Marciano (x2), Akira, A Vila, O Asilo, Julius.
Redimensiona as artes originais (2700-2800px de largura, IA) para o padrao ja
usado no blog: JPG 1600px de largura (corpo do post + fonte da capa) e um WEBP
1200px/qualidade 80 So para a capa (mesma receita de comprimir-imagens-home-blog.py).

Nao apaga nada na pasta de origem (Obras Literarias). So escreve dentro de
blog/posts/media/<slug>/.

Uso: python .claude/importar-imagens-lote-ago2026.py
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = Path(r"C:\Users\falco\OneDrive\BackUp\2. Carreira\1. JF Design\Projetos\Livros Dô\2. Produto\Catalogo\Obras Literárias")

JPG_MAX_W = 1600
JPG_QUALITY = 88
WEBP_MAX_W = 1200
WEBP_QUALITY = 80

# (slug, [(src_relative_to_SRC_ROOT, dest_filename, is_cover), ...])
POSTS = [
    ("o-marciano-satira-ficcao-cientifica-consumismo", [
        ("1. O Marciano/7. Blog/Post 1 - O Marciano/marciano_chegada_terra.jpg", "capa-portal-chegada-terra.jpg", True),
        ("1. O Marciano/7. Blog/Post 1 - O Marciano/marciano_comunicacao_digital.jpg", "multidao-conectada-celulares.jpg", False),
        ("1. O Marciano/7. Blog/Post 1 - O Marciano/marciano_fast_food_combo10.jpg", "combo-10-fast-food.jpg", False),
    ]),
    ("planeta-tanaris-amor-impossivel-ficcao-cientifica", [
        ("1. O Marciano/7. Blog/Post 2 - O Marciano - Copia/marciano_planeta_tanaris.jpg", "capa-planeta-tanaris.jpg", True),
        ("1. O Marciano/7. Blog/Post 2 - O Marciano - Copia/marciano_amor_bella.jpg", "marciano-bella-tanaris.jpg", False),
        ("1. O Marciano/7. Blog/Post 2 - O Marciano - Copia/marciano_escolha_impossivel.jpg", "escolha-impossivel-portal.jpg", False),
    ]),
    ("akira-japao-meiji-industria-belica-samurai", [
        ("11. Akira/7. Blog/O Batismo de Fogo v2 realista.jpg", "capa-batismo-de-fogo.jpg", True),
        ("11. Akira/7. Blog/A Origem em Hokkaido v2 realista.jpg", "origem-hokkaido-japao-feudal.jpg", False),
        ("11. Akira/7. Blog/O Almoço em Sapporo (O Choque de Valores).jpg", "almoco-sapporo-choque-valores.jpg", False),
    ]),
    ("resistencia-grega-romance-proibido-ocupacao-nazista", [
        ("22. A Vila/7. Blog/Post 2 - Promessa de Recomeço/Athena e o Mar Egeu (A Resiliência da Pescadora).jpg", "capa-athena-mar-egeu.jpg", True),
        ("22. A Vila/7. Blog/Post 2 - Promessa de Recomeço/A Resistência nas Montanhas (Nikos e Theo).jpg", "resistencia-montanhas-nikos-theo.jpg", False),
        ("22. A Vila/7. Blog/Post 2 - Promessa de Recomeço/Anastasia e Hans (O Amor sob as Oliveiras).jpg", "anastasia-hans-amor-proibido.jpg", False),
    ]),
    ("nazista-fugitivo-brasil-lavagem-dinheiro-asilo", [
        ("19. O Asilo/7. Blog/O Asilo São Pedro (O Casarão na Névoa).jpg", "capa-casarao-nevoa.jpg", True),
        ("19. O Asilo/7. Blog/Werner Schmidt (O Fantasma do Passado).jpg", "werner-schmidt-fantasma-passado.jpg", False),
        ("19. O Asilo/7. Blog/Dr. Carlos (A Sombra da Ganância).jpg", "dr-carlos-sombra-ganancia.jpg", False),
    ]),
    ("roma-antiga-gladiador-nazareno-pompeia", [
        ("4. Julius/7. Blog/Post 1 - A Espada do Centurião/Julius,General do Império Romano.jpg", "capa-julius-general-romano.jpg", True),
        ("4. Julius/7. Blog/Post 1 - A Espada do Centurião/A Batalha na Germânia (Julius, o Guerreiro).jpg", "batalha-germania-arena-barbara.jpg", False),
        ("4. Julius/7. Blog/Post 1 - A Espada do Centurião/Olhar do Nazareno (Julius e Yeshua na Judeia).jpg", "olhar-nazareno-julius-yeshua.jpg", False),
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
