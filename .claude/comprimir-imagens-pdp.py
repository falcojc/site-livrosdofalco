"""
Converte para WebP as imagens da PDP de O Mestre das Tormentas que sao de
fato baixadas pelo navegador (as 15 <img> do corpo + os 2 posters de video).

NAO mexe em:
- capa-oficial.jpg: so aparece em og:image/twitter:image/schema, para
  compartilhamento em redes sociais. Trocar por .webp arrisca preview quebrado
  em algum crawler mais antigo, e esse arquivo nunca e baixado por quem so
  visita a pagina (so por bots de rede social ao gerar o card do link).
- hero-cover.jpg / hero-cover-crop.jpg: nao tem nenhuma referencia em nenhum
  HTML do site (grep confirmou). Sao arquivos orfaos, ninguem baixa, entao
  nao afetam performance. Ficam ai ate alguem decidir apagar.

Gera os .webp do lado do .jpg original (mantem o .jpg, nao apaga nada).
Uso: python .claude/comprimir-imagens-pdp.py
"""
from pathlib import Path
from PIL import Image

MEDIA = Path(__file__).resolve().parent.parent / "o-mestre-das-tormentas" / "media"

# nome -> largura maxima em pixel, calculada a partir da coluna do grid onde
# a imagem aparece (CSS do proprio arquivo) x2 pra retina. Nao ha por que
# guardar pixel que nenhuma tela vai mostrar.
CONVERTER = {
    "logo-emblema.jpg": 1000,        # .cover-feature, width:100% da .wrap (1180px)
    "timeline-infancia.jpg": 800,    # .timeline, grid de 4 colunas (~295px, 2x retina)
    "timeline-juventude.jpg": 800,
    "timeline-ascensao.jpg": 800,
    "timeline-lenda.jpg": 800,
    "mapa-mundi.jpg": 1600,          # .map-bg, imagem de fundo larga
    "personagem-john-storm.jpg": 800,  # .chars, grid de 3 colunas (~375px, 2x retina)
    "personagem-marisol.jpg": 800,
    "personagem-feng-long.jpg": 800,
    "momento-batismo.jpg": 1200,     # .moments, grid de 2 colunas (~578px, 2x retina)
    "momento-duelo.jpg": 1200,
    "momento-furacao.jpg": 1200,
    "momento-malaca.jpg": 1200,
    "podcast-cover.jpg": 500,        # .podcast-card, coluna fixa de 200px
    "banner-amazon.jpg": 1200,       # .cta-banner, max-width:900px
    "hero-poster.jpg": 1280,         # poster do video hero, mantem tamanho original
    "trailer-cover.jpg": 1000,       # poster do video trailer, coluna ~600px do grid
}

QUALITY = 80

def main():
    total_antes = 0
    total_depois = 0
    for name, max_w in CONVERTER.items():
        src = MEDIA / name
        if not src.exists():
            print(f"AVISO: {name} nao encontrado, pulando")
            continue
        dst = src.with_suffix(".webp")
        img = Image.open(src).convert("RGB")
        if img.width > max_w:
            new_h = round(img.height * max_w / img.width)
            img = img.resize((max_w, new_h), Image.LANCZOS)
        img.save(dst, "WEBP", quality=QUALITY, method=6)
        antes = src.stat().st_size
        depois = dst.stat().st_size
        total_antes += antes
        total_depois += depois
        print(f"{name:35s} {antes/1024:7.0f} KB -> {depois/1024:7.0f} KB  ({100*(1-depois/antes):.0f}% menor)")
    print("-" * 60)
    print(f"TOTAL: {total_antes/1024:.0f} KB -> {total_depois/1024:.0f} KB "
          f"({100*(1-total_depois/total_antes):.0f}% de reducao)")

if __name__ == "__main__":
    main()
