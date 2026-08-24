# -*- coding: utf-8 -*-
"""Converte as artes de cena da LP /romance-historico para WebP servivel na web.

As originais sao 2816x1536 e pesam de 2,8 a 12,3 MB. Servidas assim, elas sozinhas
destroem o orcamento de performance da pagina. Aqui elas viram WebP de ~800px, que
e o dobro da largura renderizada da ficha (367px numa grade de 3 colunas em 1180px),
o suficiente para tela retina sem desperdicio.

Idempotente: rodar de novo so regrava a saida, nunca toca no original.

Resolucao de caminho sem hardcode, porque o Falco reorganiza a arvore de pastas:
sobe ate achar o diretorio do projeto pelo NOME do diretorio, nunca pelo caminho
completo (a raiz de tudo e "...\\OneDrive\\BackUp\\...", entao filtrar por "backup"
no caminho inteiro descartaria o projeto).
"""
import os
import subprocess
import sys

LARGURA = 800
QUALIDADE = 80  # escala do libwebp: 0 a 100

# arquivo de origem -> (slug da obra, crop opcional "w:h:x:y" na resolucao original)
# Troca de 24/08 (segunda rodada): as tres cenas originais nao tinham estilo em
# comum (ilustracao quente, CGI escuro de naufragio, still cinematografico) e
# duas delas nao mostravam pessoa nenhuma. Trocadas por arte com personagem em
# cena, mais parecido com o padrao retrato do /arquetipos.
CENAS = {
    # Matteo mora em 2. Produto/Personagens, nao em StoryTelling/Romance Historico
    # (unico caso: fica em pasta diferente das outras tres) -- sobe 2 niveis
    "../../Personagens/Matteo, O Patriarca (O Siciliano).png": ("o-siciliano-matteo", None),
    # Original e retrato (1536x2730). Crop pre-scale pra paisagem 1536x1050
    # (cabeca ate a coxa + fogueira + mar), testado visualmente antes de entrar.
    "3 - Adulto 3 - John Storm.png": ("mestre-das-tormentas-fogueira", "1536:1050:0:830"),
    "O Romance Clandestino (Paco e Carmen sob a Tempestade).jpg": ("amor-e-odio-clandestino", None),
    "Dante e Helga - O Passeio e a Conexão no Mar.png": ("o-comandante-dante-helga", None),
}


def raiz_do_projeto():
    """Sobe a arvore ate o diretorio chamado 'Livros Dô'."""
    d = os.path.abspath(__file__)
    while True:
        d, nome = os.path.split(d)
        if nome == "Livros Dô":
            return os.path.join(d, nome)
        if not nome:
            sys.exit("nao achei a raiz do projeto ('Livros Dô') subindo a partir do script")


def main():
    raiz = raiz_do_projeto()
    origem = os.path.join(raiz, "2. Produto", "StoryTelling", "Romance Histórico")
    destino = os.path.join(raiz, "Site", "livrosdofalco", "romance-historico", "media")
    os.makedirs(destino, exist_ok=True)

    if not os.path.isdir(origem):
        sys.exit(f"pasta de origem nao encontrada: {origem}")

    total_antes = total_depois = 0
    for arquivo, (slug, crop) in CENAS.items():
        entrada = os.path.join(origem, arquivo)
        if not os.path.isfile(entrada):
            print(f"  AUSENTE, pulando: {arquivo}")
            continue
        saida = os.path.join(destino, f"{slug}.webp")
        # -vf scale: altura -2 mantem a proporcao e forca numero par
        # -compression_level 6: mais lento na geracao, menor no resultado
        # crop opcional roda ANTES do scale, pra nao pagar peso de pixel que
        # nunca aparece na tela (o original fica intocado de qualquer jeito)
        filtro = f"crop={crop}," if crop else ""
        filtro += f"scale={LARGURA}:-2:flags=lanczos"
        cmd = [
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", entrada,
            "-vf", filtro,
            "-c:v", "libwebp", "-quality", str(QUALIDADE), "-compression_level", "6",
            saida,
        ]
        subprocess.run(cmd, check=True)
        antes = os.path.getsize(entrada) / 1024
        depois = os.path.getsize(saida) / 1024
        total_antes += antes
        total_depois += depois
        print(f"  {slug}.webp  {antes/1024:.1f} MB -> {depois:.0f} KB")

    if total_antes:
        print(f"\ntotal: {total_antes/1024:.1f} MB -> {total_depois:.0f} KB "
              f"({100 - total_depois/total_antes*100:.1f}% menor)")
    print("destino:", destino)


if __name__ == "__main__":
    main()
