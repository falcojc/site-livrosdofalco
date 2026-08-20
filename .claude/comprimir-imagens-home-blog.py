"""
Converte para WebP as imagens da home (banners do hero + logo do menu) e as
capas dos posts do blog (13 no total, 9 aparecem no carrossel da home, as
outras 4 so no /blog/ e na propria pagina do post).

Limites de largura escolhidos por onde cada imagem de fato aparece:
- banners: hero em tela cheia, com overlay escuro forte por cima (a foto
  nunca precisa de nitidez de perto). 1600px cobre qualquer desktop real.
- capas de post: aparecem pequenas no teaser da home (~398px), mas a MESMA
  imagem tambem e a capa cheia dentro do post (article.post{max-width:720px}
  no CSS). O corte usa o maior uso (720px x ~1,7 = 1200px), pra nao deixar a
  capa do post borrada.
- pictograma (logo do menu): PNG com transparencia, mantido RGBA. Aparece a
  46x33px em 9 lugares do site, 150px de corte da bastante folga de retina.

Gera .webp do lado do arquivo original, NAO apaga o .jpg/.png original.
Uso: python .claude/comprimir-imagens-home-blog.py
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent

BANNERS = [
    "banners/banner-1-universo-epico.jpg",
    "banners/banner-2-forca-feminina.jpg",
    "banners/banner-3-misterio.jpg",
    "banners/banner-4-jornada-epica.jpg",
    "banners/banner-5-cta.jpg",
]
BANNER_MAX_W = 1600

BLOG_COVERS = [
    "blog/posts/media/a-lenda-dos-sete-mares/capa-navio-tempestade.jpg",
    "blog/posts/media/bussola-moral-guerra-vida-comum-europa/capa-casal-neblina-europa.jpg",
    "blog/posts/media/desafios-expedicoes-floresta-amazonica/capa-rio-floresta-amazonica.jpg",
    "blog/posts/media/fascinante-perigosa-milenar-rota-da-seda/capa-caravana-deserto.jpg",
    "blog/posts/media/guerra-fria-asia-espionagem-mi6-kgb-hong-kong/capa-hong-kong-neon.jpg",
    "blog/posts/media/guerra-secessao-corrida-ouro-justica/capa-resistencia-esperanca.jpg",
    "blog/posts/media/imigracao-italiana-jornada-mediterraneo-cafezais/capa-porto-navio-imigrantes.jpg",
    "blog/posts/media/lei-seca-anos-20-submundo-nova-york/capa-rua-little-italy.jpg",
    "blog/posts/media/vida-real-nos-sete-mares/capa-frota-tempestade.jpg",
    "blog/posts/media/operacao-avalanche-salerno-segunda-guerra/capa-operacao-avalanche-salerno.jpg",
    "blog/posts/media/papel-mulher-japao-feudal/capa-mulher-rua-tradicional.jpg",
    "blog/posts/media/revolucao-do-conteiner-porto-genova/capa-caos-do-cais.jpg",
    "blog/posts/media/segredos-cabares-belle-epoque-paris/capa-fachada-cabare.jpg",
]
BLOG_MAX_W = 1200

QUALITY = 80

def convert_rgb(rel_path, max_w):
    src = ROOT / rel_path
    if not src.exists():
        print(f"AVISO: {rel_path} nao encontrado, pulando")
        return 0, 0
    dst = src.with_suffix(".webp")
    img = Image.open(src).convert("RGB")
    if img.width > max_w:
        new_h = round(img.height * max_w / img.width)
        img = img.resize((max_w, new_h), Image.LANCZOS)
    img.save(dst, "WEBP", quality=QUALITY, method=6)
    antes, depois = src.stat().st_size, dst.stat().st_size
    print(f"{rel_path:75s} {antes/1024:7.0f} KB -> {depois/1024:7.0f} KB ({100*(1-depois/antes):.0f}% menor)")
    return antes, depois

def convert_logo():
    src = ROOT / "pictograma-livrosdofalco.png"
    dst = src.with_suffix(".webp")
    img = Image.open(src).convert("RGBA")
    max_w = 150
    if img.width > max_w:
        new_h = round(img.height * max_w / img.width)
        img = img.resize((max_w, new_h), Image.LANCZOS)
    img.save(dst, "WEBP", quality=90, method=6)
    antes, depois = src.stat().st_size, dst.stat().st_size
    print(f"{'pictograma-livrosdofalco.png (RGBA, mantem transparencia)':75s} {antes/1024:7.0f} KB -> {depois/1024:7.0f} KB ({100*(1-depois/antes):.0f}% menor)")
    return antes, depois

def main():
    total_antes = total_depois = 0
    print("--- banners (hero da home) ---")
    for p in BANNERS:
        a, d = convert_rgb(p, BANNER_MAX_W)
        total_antes += a; total_depois += d
    print("--- capas de post do blog ---")
    for p in BLOG_COVERS:
        a, d = convert_rgb(p, BLOG_MAX_W)
        total_antes += a; total_depois += d
    print("--- logo do menu ---")
    a, d = convert_logo()
    total_antes += a; total_depois += d
    print("-" * 70)
    print(f"TOTAL: {total_antes/1024:.0f} KB -> {total_depois/1024:.0f} KB ({100*(1-total_depois/total_antes):.0f}% de reducao)")

if __name__ == "__main__":
    main()
