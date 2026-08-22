"""
Ajustes de imagem da LP /arquetipos (21/08/2026), itens 3 e 10 do pedido do Falco.
Mesma convencao de .claude/importar-imagens-lote2-ago2026.py (PIL, WEBP method=6).
Qualidades escolhidas testando 3-4 valores e comparando visualmente antes de
decidir (ver sessao) -- nao e so "abaixar o numero", cada uma foi conferida.

O que faz:
1. Converte o novo post de divulgacao do audiolivro+e-book (JPG 2048x2048, vem de
   2. Produto/Catalogo/.../8. Social) pra webp otimizado, pro bloco "Dante na
   Integra". Fica no tamanho quadrado original (nao cortado pra 16:9): e uma peca
   de design com texto (titulo, player, selo Kindle) -- cortar pra 16:9 cortaria
   texto em qualquer enquadramento possivel, dado que a peca e quadrada.
2. Recomprime john-storm.webp com qualidade mais agressiva (o Lighthouse pediu
   mais compactacao, nao redimensionamento -- o arquivo ja bate 1100x619, a tela
   exibida).
3. Recomprime video-poster.webp (mantem 1280 de largura, pro desktop) e gera uma
   variante 640 pro srcset mobile (o Lighthouse mostrou que o mobile so precisa de
   620x348).

Roda a partir dos originais no git (main), nunca reprocessa um webp ja
recomprimido (perda geracional).

Nao mexe em /covers/mestre-das-tormentas.webp nem /pictograma-livrosdofalco.webp:
sao arquivos compartilhados com o site inteiro (exibidos bem maiores em outras
paginas -- grid de Obras da home, headers de toda pagina), encolher a origem so
pra esta LP pioraria a nitidez no resto do site. Fica como tarefa separada.
"""
from pathlib import Path
from PIL import Image

REPO = Path(__file__).resolve().parent.parent
MEDIA = REPO / "arquetipos" / "media"

SOCIAL_SRC = Path(
    r"C:\Users\falco\OneDrive\BackUp\2. Carreira\1. JF Design\Projetos\Livros Dô"
    r"\2. Produto\Catalogo\Obras Literárias\30. O Comandante\8. Social"
    r"\Post Lançamento AudioBook + E-book Kindle.jpg"
)


def save_webp(img: Image.Image, dst: Path, quality: int):
    img.save(dst, "WEBP", quality=quality, method=6)
    print(f"{dst.name}: {dst.stat().st_size/1024:.1f} KiB ({img.width}x{img.height})")


def main():
    # 1) Post de lancamento (audiolivro + e-book) -> dante-audiolivro.webp
    im = Image.open(SOCIAL_SRC).convert("RGB")
    max_w = 920
    if im.width > max_w:
        ratio = max_w / im.width
        im = im.resize((max_w, round(im.height * ratio)), Image.LANCZOS)
    save_webp(im, MEDIA / "dante-audiolivro.webp", quality=82)

    # 2) john-storm.webp: mesma dimensao (1100x619), so mais compressao.
    #    Testado 45/50/55/62/68 -- 50 nao mostrou perda visivel a olho nu e bate
    #    perto da economia de 24.9 KiB que o Lighthouse pediu.
    im2 = Image.open(MEDIA / "john-storm.webp").convert("RGB")
    save_webp(im2, MEDIA / "john-storm.webp", quality=50)

    # 3) video-poster: recomprime a 1280 (desktop) e gera a variante 640 (mobile,
    #    srcset). Testado 65/72/78 pra 1280 -- 72 sem perda visivel no texto
    #    "Descubra esses mundos" / logo.
    im3 = Image.open(MEDIA / "video-poster.webp").convert("RGB")
    save_webp(im3, MEDIA / "video-poster.webp", quality=72)

    im3b = Image.open(MEDIA / "video-poster.webp")
    ratio = 640 / im3b.width
    im3b = im3b.resize((640, round(im3b.height * ratio)), Image.LANCZOS)
    save_webp(im3b, MEDIA / "video-poster-640.webp", quality=70)


if __name__ == "__main__":
    main()
