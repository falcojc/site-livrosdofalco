"""
Terceira rodada de compressao de imagem, depois que o segundo PageSpeed (pos
lote 2) apontou o que sobrou: a pasta personagens/ inteira (15 fotos, nunca
tocada), as 30 capas de livro da galeria "As Obras" (tambem nunca tocadas,
mas ja vem em dimensao modesta, o ganho principal aqui e so trocar de
formato), e uma folga extra de compactacao nos banners/capas de blog que
ja viraram WebP na rodada anterior (o Lighthouse passou a pedir "aumentar
compactacao" em vez de "usar formato moderno", ou seja, qualidade 80 ainda
tinha gordura).

- personagens/: sem corte de dimensao (os arquivos ja sao modestos, 900x502
  a 1280x720; cortar mais deixaria a imagem no limite pro crop retina do
  grid de 3 colunas). So troca de formato.
- covers/: corte leve de 500px (so afeta os 6 arquivos que hoje sao 600px
  de largura). o-comandante-quadrada.jpg fica de fora (so aparece em
  og:image do audiolivro, igual capa-oficial.jpg da PDP).
- banners/ e blog/posts/media/ (as 13 capas de post): reconvertidas com
  qualidade mais baixa (70 em vez de 80), MESMA dimensao de corte de antes.
  Sobrescreve o .webp que ja existe, nao mexe no .jpg original.

Uso: python .claude/comprimir-imagens-rodada3.py
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent

def convert(rel_path, max_w=None, quality=78):
    src = ROOT / rel_path
    if not src.exists():
        print(f"AVISO: {rel_path} nao encontrado, pulando")
        return 0, 0
    dst = src.with_suffix(".webp")
    img = Image.open(src).convert("RGB")
    if max_w and img.width > max_w:
        new_h = round(img.height * max_w / img.width)
        img = img.resize((max_w, new_h), Image.LANCZOS)
    img.save(dst, "WEBP", quality=quality, method=6)
    antes, depois = src.stat().st_size, dst.stat().st_size
    print(f"{rel_path:60s} {antes/1024:7.0f} KB -> {depois/1024:7.0f} KB ({100*(1-depois/antes):.0f}% menor)")
    return antes, depois

PERSONAGENS = [f"personagens/{n}.jpg" for n in [
    "aruatam", "athena", "bela", "dom-domenico", "james", "jesuita", "joana",
    "joca", "john-storm", "julius", "katia", "matteo", "sem-nome", "will", "yoko",
]]

COVERS = [f"covers/{n}.jpg" for n in [
    "a-casa-dos-prazeres", "a-industria-do-vicio", "a-saga-italiana", "a-teia",
    "a-viagem", "a-vila", "akira", "amor-e-odio", "destinos-cruzados-parte-2",
    "destinos-cruzados", "joana", "julius", "mariana-e-jose-inacio",
    "mestre-das-tormentas", "o-asilo", "o-comandante-mini", "o-comandante",
    "o-explorador-desconhecido", "o-explorador", "o-jesuita", "o-marciano",
    "o-que-eu-lembro-deles", "o-reino", "o-siciliano", "o-tesouro-maldito",
    "os-dois-irmaos", "os-italianos", "os-refugiados", "os-templarios",
    "reflexoes-sobre-a-vida", "sangue-frio", "um-lugar-ao-sol",
    # o-comandante-quadrada.jpg fica de fora: so aparece em og:image
]]

BANNERS = [f"banners/{n}.jpg" for n in [
    "banner-1-universo-epico", "banner-2-forca-feminina", "banner-3-misterio",
    "banner-4-jornada-epica", "banner-5-cta",
]]

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

def main():
    total_a = total_d = 0
    print("--- personagens (sem corte de dimensao) ---")
    for p in PERSONAGENS:
        a, d = convert(p, max_w=None, quality=78)
        total_a += a; total_d += d
    print("--- capas de livro (corte leve, 500px) ---")
    for p in COVERS:
        a, d = convert(p, max_w=500, quality=78)
        total_a += a; total_d += d
    print("--- banners: reconvertidos, qualidade 70 (era 80) ---")
    for p in BANNERS:
        a, d = convert(p, max_w=1600, quality=70)
        total_a += a; total_d += d
    print("--- capas de post: reconvertidas, qualidade 70 (era 80) ---")
    for p in BLOG_COVERS:
        a, d = convert(p, max_w=1200, quality=70)
        total_a += a; total_d += d
    print("-" * 70)
    print(f"TOTAL: {total_a/1024:.0f} KB -> {total_d/1024:.0f} KB ({100*(1-total_d/total_a):.0f}% de reducao)")

if __name__ == "__main__":
    main()
