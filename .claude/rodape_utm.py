# -*- coding: utf-8 -*-
"""
Coloca UTM no link do rodape para a Falco Strategy, com utm_content por
secao do site.

Sem UTM o GA4 da FS ja veria isso como referral de livrosdofalco.com.br,
entao o ganho nao e "passar a medir", e saber DE ONDE dentro do site a
pessoa clicou: home, blog, LP ou pagina de categoria. Isso responde se o
credito no rodape vale alguma coisa como canal ou se e so assinatura.

utm_medium=referral de proposito: qualquer outro valor faria o GA4 da FS
classificar o trafego fora do canal Referral e sujar a comparacao com o
resto do trafego de indicacao.

Idempotente. Uso: python .claude/rodape_utm.py [--dry-run]
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = "https://falcostrategy.com.br"
SOURCE = "livrosdofalco"
CAMPANHA = "rodape-credito"

# Caminho do arquivo -> nome da secao no utm_content. Primeiro que casar vence.
SECOES = [
    ("_includes/base.njk", "blog"),
    ("audiolivro/obrigado", "lp-audiolivro-obrigado"),
    ("audiolivro", "lp-audiolivro"),
    ("newsletter", "newsletter"),
    ("arquetipos", "arquetipos"),
    ("o-mestre-das-tormentas", "pdp-mestre-tormentas"),
    ("categoria/index.html", "categoria-hub"),
    ("categoria/", "categoria"),
    ("index.html", "home"),
]


def secao(rel):
    for chave, nome in SECOES:
        if chave in rel:
            return nome
    return "outro"


alvos = [p for p in list(RAIZ.rglob("*.html")) + list(RAIZ.rglob("*.njk"))
         if "node_modules" not in p.parts and "_site" not in p.parts
         and "falcostrategy" in p.read_text(encoding="utf-8", errors="ignore").lower()]

feitos = []
for arq in sorted(alvos):
    rel = arq.relative_to(RAIZ).as_posix()
    html = arq.read_text(encoding="utf-8")
    alvo = (f"{DESTINO}/?utm_source={SOURCE}&amp;utm_medium=referral"
            f"&amp;utm_campaign={CAMPANHA}&amp;utm_content={secao(rel)}")
    # Casa a URL atual com ou sem UTM, entao rodar de novo so atualiza.
    novo, n = re.subn(r'href="https://falcostrategy\.com\.br[^"]*"',
                      f'href="{alvo}"', html)
    if n and novo != html:
        if "--dry-run" not in sys.argv:
            arq.write_text(novo, encoding="utf-8")
        feitos.append((rel, secao(rel), n))
    elif n:
        feitos.append((rel, secao(rel) + " (ja estava)", n))

for rel, sec, n in feitos:
    print(f"  {rel:48s} utm_content={sec}")
print(f"\n{len(feitos)} arquivos, {sum(n for _, _, n in feitos)} links")
if "--dry-run" in sys.argv:
    print("(dry-run, nada escrito)")
