"""
Quarta rodada de compressao de imagem, a partir do PageSpeed de 24/08 (84 de
desempenho, LCP 4,4s). O relatorio apontou 209 KiB de economia estimada em
11 arquivos especificos: 5 personagens que sobraram da rodada 3 (bela, katia,
matteo, athena, john-storm — a rodada 3 So trocou formato, nao reapertou
qualidade), a capa do omnibus "A Saga Italiana", o slide 1 do hero (unico
banner carregado no load, os outros 4 sao lazy e por isso nao aparecem no
relatorio), e 3 capas de post de blog.

Qualidade por arquivo foi escolhida testando visualmente (nao só batendo o
numero do PageSpeed), porque a mesma queda de qualidade WebP tem efeito bem
diferente dependendo do quanto a imagem e reduzida na tela:
- personagens/: fonte grande (900-1280px) exibida pequena (~356-370px de
  card, 3 colunas), entao aguenta quality bem baixo sem artefato visivel.
  bela e o arquivo mais "ruidoso" (folhagem, muita textura) e por isso o que
  mais precisou cair (35) pra chegar perto da economia estimada.
- banners/banner-1-800w: e o hero, fetchpriority=high, primeira coisa que a
  pessoa ve em tela cheia — aqui fui conservador (55) mesmo nao batendo 100%
  da estimativa do PageSpeed, testado com zoom 3x na estante de livros (a
  area com mais textura) sem diferenca visivel a olho nu.
- capas de post: exibidas quase no tamanho nativo (700 de 760px, so 8% de
  folga), tambem conservador.

joana.webp e o unico com problema de DIMENSAO, nao so compactacao: e uma
foto retrato (720x1280) dentro de um card paisagem (aspect-ratio 3/4 via
object-fit:cover + object-position:center 15%), entao so ~75% da altura
aparece em tela e o resto e puro desperdicio de bytes. O corte abaixo
reproduz matematicamente o mesmo enquadramento que a CSS ja mostra (formula
do object-position: offset = overflow * 0.15), entao o crop fica idêntico ao
que já era visível, so sem os pixels que a CSS sempre cortou. Conferido
visualmente antes de aplicar.

covers/a-saga-italiana.webp tem mesma proporcao do que e exibido (so estava
1,3x maior que o necessario), entao reduz e comprime sem cortar nada — o
width/height do <img> em index.html e categoria/raizes-sacrificio-familia
precisam ser atualizados junto (480x718 -> 400x598), senao o navegador
reserva o espaco errado (CLS).

Sobrescreve os .webp existentes. Nao mexe em nenhum arquivo fonte fora da
lista abaixo. Uso: python .claude/comprimir-imagens-rodada4.py
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent


def recompress(rel_path, quality, method=6):
    p = ROOT / rel_path
    img = Image.open(p).convert("RGB")
    antes = p.stat().st_size
    img.save(p, "WEBP", quality=quality, method=method)
    depois = p.stat().st_size
    print(f"{rel_path:90s} {antes/1024:7.1f} KiB -> {depois/1024:7.1f} KiB ({100*(1-depois/antes):.0f}% menor)")
    return antes, depois


def crop_and_compress(rel_path, box, quality, method=6):
    """box = (left, top, right, bottom) em pixels da imagem original."""
    p = ROOT / rel_path
    img = Image.open(p).convert("RGB")
    antes = p.stat().st_size
    cropped = img.crop(box)
    cropped.save(p, "WEBP", quality=quality, method=method)
    depois = p.stat().st_size
    print(f"{rel_path:90s} {antes/1024:7.1f} KiB -> {depois/1024:7.1f} KiB ({100*(1-depois/antes):.0f}% menor, corte {img.size}->{cropped.size})")
    return antes, depois


def resize_and_compress(rel_path, target_w, quality, method=6):
    p = ROOT / rel_path
    img = Image.open(p).convert("RGB")
    antes = p.stat().st_size
    w, h = img.size
    new_h = round(h * target_w / w)
    resized = img.resize((target_w, new_h), Image.LANCZOS)
    resized.save(p, "WEBP", quality=quality, method=method)
    depois = p.stat().st_size
    print(f"{rel_path:90s} {antes/1024:7.1f} KiB -> {depois/1024:7.1f} KiB ({100*(1-depois/antes):.0f}% menor, {img.size}->{resized.size})")
    return antes, depois, resized.size


def main():
    total_a = total_d = 0

    print("--- personagens: so reaperta qualidade, sem cortar dimensao ---")
    for rel, q in [
        ("personagens/bela.webp", 35),
        ("personagens/katia.webp", 50),
        ("personagens/matteo.webp", 50),
        ("personagens/athena.webp", 50),
        ("personagens/john-storm.webp", 60),
    ]:
        a, d = recompress(rel, q)
        total_a += a; total_d += d

    print("--- joana: corte pro mesmo enquadramento que a CSS ja mostra ---")
    a, d = crop_and_compress("personagens/joana.webp", (0, 48, 720, 1008), 68)
    total_a += a; total_d += d

    print("--- capa A Saga Italiana: reduz pra tamanho exibido + comprime ---")
    a, d, new_size = resize_and_compress("covers/a-saga-italiana.webp", 400, 55)
    total_a += a; total_d += d
    print(f"    NOVO TAMANHO: {new_size[0]}x{new_size[1]} — atualizar width/height no HTML")

    print("--- banner 1 (hero, LCP): conservador, e a primeira coisa em tela ---")
    a, d = recompress("banners/banner-1-universo-epico-800w.webp", 55)
    total_a += a; total_d += d

    print("--- capas de post do blog ---")
    for rel, q in [
        ("blog/posts/media/guerra-secessao-corrida-ouro-justica/capa-resistencia-esperanca-760w.webp", 45),
        ("blog/posts/media/imigracao-italiana-jornada-mediterraneo-cafezais/capa-porto-navio-imigrantes-760w.webp", 65),
        ("blog/posts/media/desafios-expedicoes-floresta-amazonica/capa-rio-floresta-amazonica-760w.webp", 70),
    ]:
        a, d = recompress(rel, q)
        total_a += a; total_d += d

    print("-" * 100)
    print(f"TOTAL: {total_a/1024:.0f} KiB -> {total_d/1024:.0f} KiB (economia de {(total_a-total_d)/1024:.0f} KiB)")


if __name__ == "__main__":
    main()
