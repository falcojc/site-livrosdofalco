"""
Aperta o enquadramento da capa do omnibus Destinos Cruzados: Os Fios do
Destino. A arte tem 3 paineis (Delhi / trem / Hong Kong) e termina com uma
faixa preta grande para caber o nome do autor: entre a borda dourada do
3o painel e o texto "Domenico Falco" havia ~150px de preto morto, mais outra
sobra abaixo do nome. Numa capa de PDP exibida pequena (118-260px de largura),
essa sobra fazia a arte parecer mais espichada/vazia que as capas das outras
obras da onda (O Siciliano, A Vila, Um Lugar ao Sol), que nao tem essa faixa.

Fix: corta a faixa morta em duas fatias que se encontram no preto puro dos
dois lados (sem risco de emenda visivel) e cola de volta, sem tocar em
nenhum pixel de arte ou texto. Proporcao sai de 1.61 para 1.43 (dentro da
faixa 1.34-1.61 que ja existe entre as 30 obras do catalogo).

Toca os 3 destinos que nascem da mesma fonte:
  1. .claude/epub/capas/destinos-cruzados-omnibus.jpg  (motor de EPUB + PDP)
  2. Site/livrosdofalco/covers/destinos-cruzados-fios-do-destino.{jpg,webp}
  3. Site/livrosdofalco/covers/pdp/destinos-cruzados-fios-do-destino-*
     (regerado por .claude/pdp/gerar_capas.py depois deste script, nao aqui)

Uso: python .claude/recorte-capa-destinos-cruzados-omnibus-05-09-2026.py
"""
from pathlib import Path
from PIL import Image

SITE_ROOT = Path(__file__).resolve().parent.parent
RAIZ = SITE_ROOT.parent.parent
# Le do original intocado (nao do .claude/epub/capas, que este script
# sobrescreve): assim rodar o script duas vezes sempre corta a partir da
# mesma arte, em vez de cortar em cima do proprio resultado anterior.
ORIGINAL = (RAIZ / "2. Produto" / "Catalogo" / "Omnibus" / "Destinos Cruzados"
            / "3. capa" / "Capa Destinos Cruzados Omnibus.jpg")
DESTINO_CANONICO = RAIZ / ".claude" / "epub" / "capas" / "destinos-cruzados-omnibus.jpg"
SLUG = "destinos-cruzados-fios-do-destino"

# Limites medidos por perfil de brilho (media de linha), amostrados a cada
# poucos pixels: y=2280 e ja preto solido (a borda dourada do 3o painel
# desaparece por volta de 2270); o texto do autor comeca a aparecer perto de
# 2394 e termina perto de 2448. Cortar em 2280/2340 preserva ~60px de
# respiro puro-preto antes do nome, contra os ~150px originais. Do lado de
# baixo, a imagem original ainda sobrava ~80px de preto puro depois do nome;
# CORTE_FUNDO_ATE encurta essa margem para ~40px.
CORTE_TOPO_ATE = 2280
CORTE_FUNDO_DE = 2340
CORTE_FUNDO_ATE = 2488

LARGURA_SITE = 400
JPG_QUALITY = 85
WEBP_QUALITY = 68


def main():
    original = Image.open(ORIGINAL).convert("RGB")
    w, h = original.size
    topo = original.crop((0, 0, w, CORTE_TOPO_ATE))
    fundo = original.crop((0, CORTE_FUNDO_DE, w, CORTE_FUNDO_ATE))
    apertada = Image.new("RGB", (w, topo.height + fundo.height))
    apertada.paste(topo, (0, 0))
    apertada.paste(fundo, (0, topo.height))
    print(f"{original.size} (proporcao {h/w:.3f}) -> {apertada.size} "
          f"(proporcao {apertada.height/apertada.width:.3f})")

    apertada.save(DESTINO_CANONICO, "JPEG", quality=92, optimize=True, progressive=True)
    print(f"fonte canonica atualizada: {DESTINO_CANONICO.relative_to(RAIZ)}")

    largura = LARGURA_SITE
    altura = round(apertada.height * largura / apertada.width)
    card = apertada.resize((largura, altura), Image.LANCZOS)
    jpg_out = SITE_ROOT / "covers" / f"{SLUG}.jpg"
    webp_out = SITE_ROOT / "covers" / f"{SLUG}.webp"
    card.save(jpg_out, "JPEG", quality=JPG_QUALITY, optimize=True)
    card.save(webp_out, "WEBP", quality=WEBP_QUALITY, method=6)
    print(f"covers: {card.size} -> {jpg_out.name}, {webp_out.name}")
    print("falta rodar: python .claude/pdp/gerar_capas.py "
          "destinos-cruzados-fios-do-destino")


if __name__ == "__main__":
    main()
