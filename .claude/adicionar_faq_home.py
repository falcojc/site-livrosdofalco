# -*- coding: utf-8 -*-
"""
Insere a secao de Perguntas Frequentes visivel na home.

Por que visivel e nao so JSON-LD: a diretriz do Google exige que o conteudo
marcado como FAQPage esteja visivel na pagina. Marcar sem o texto na tela e
violacao, nao atalho.

Por que na home e nao numa pagina /faq: e a pagina onde o anuncio pousa, e o
texto das respostas usa o bigrama literal "romance historico", que e o termo
limitado por baixa qualidade de landing page no Google Ads.

Sem link para titulo de obra de proposito: metade dos cards citados fica
escondida atras do "ver mais" (display:none), e ancora para elemento
escondido nao rola a pagina.

Idempotente. Uso: python .claude/adicionar_faq_home.py [--dry-run]
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
INDEX = RAIZ / "index.html"

CSS = """
  /* Perguntas frequentes: texto visivel que sustenta o FAQPage do JSON-LD */
  .faq-section{background:var(--bg);border-top:1px solid var(--card-border);}
  .faq-section .sec-head{max-width:680px;margin:0 auto 44px;text-align:center;}
  .faq-section .eyebrow{justify-content:center;}
  .faq-section .divider{margin:18px auto 0;}
  .faq-list{max-width:820px;margin:0 auto;display:grid;gap:14px;}
  .faq-item{background:var(--card);border:1px solid var(--card-border);border-radius:10px;}
  .faq-item summary{cursor:pointer;list-style:none;padding:18px 22px;display:flex;
    justify-content:space-between;align-items:center;gap:18px;
    font-family:'Cinzel',serif;font-size:16px;letter-spacing:.01em;color:var(--text);}
  .faq-item summary::-webkit-details-marker{display:none;}
  .faq-item summary::after{content:'+';color:var(--gold);font-size:22px;line-height:1;flex:none;}
  .faq-item[open] summary::after{content:'\\2013';}
  .faq-item summary:hover{color:var(--gold-bright);}
  .faq-item summary:focus-visible{outline:2px solid var(--gold);outline-offset:2px;}
  .faq-answer{padding:0 22px 20px;color:var(--text-muted);font-size:17px;line-height:1.75;}
  .faq-answer a{color:var(--gold-bright);}
  @media(max-width:620px){
    .faq-item summary{font-size:15px;padding:16px 18px;}
    .faq-answer{padding:0 18px 18px;font-size:16px;}
  }
"""

PERGUNTAS = [
    ("Quem é Domenico Falco?",
     "Escritor brasileiro de romance histórico, autor de trinta romances ambientados em seis "
     "países e quatro séculos. Do Japão imperial à Belle Époque, da Rota da Seda à corrida do "
     "ouro, os livros partem sempre da mesma pergunta: até onde você vai pela sua família, e o "
     "que isso te custa?"),
    ("Por qual livro de Domenico Falco começar?",
     "Depende do que te move. Para família e sacrifício, <em>Os Dois Irmãos</em>. Para uma "
     "protagonista que decide o próprio destino, <em>Joana: A Dama da Noite</em>. Para aventura "
     "no mar, <em>O Mestre das Tormentas</em>. Para começar pelo mais recente, "
     "<em>O Comandante</em>."),
    ("Os romances são baseados em fatos reais?",
     "Os personagens são ficção, o cenário não. Cada livro parte de pesquisa histórica sobre "
     "eventos, lugares e costumes reais do período: a imigração italiana, a ocupação nazista na "
     "Grécia, o fim do xogunato, a revolução do contêiner no porto de Gênova."),
    ("Existe uma ordem de leitura?",
     "A maioria é independente e pode ser lida em qualquer ordem. Três formam um arco cronológico "
     "da diáspora italiana: <em>Os Dois Irmãos</em> (1860), <em>O Siciliano</em> (início do século "
     "XX) e <em>Os Italianos</em> (pós-guerra), reunidos também na edição "
     "<a href=\"#a-saga-italiana\">A Saga Italiana</a>."),
    ("Existe audiolivro?",
     "Sim. <em>O Comandante</em> tem audiolivro completo em MP3, capítulo por capítulo, para "
     "ouvir offline. É gratuito: você informa o e-mail e "
     "<a href=\"/audiolivro\">recebe os arquivos para baixar</a>."),
    ("Onde comprar os livros?",
     "Todos os romances estão na Amazon, em Kindle e capa comum, e vários no Kindle Unlimited. "
     "O catálogo completo, com sinopse e link de cada obra, está "
     "<a href=\"#obras\">na seção Obras</a>."),
]


def montar_html():
    itens = []
    for i, (p, r) in enumerate(PERGUNTAS):
        aberto = " open" if i == 0 else ""
        itens.append(
            f'      <details class="faq-item"{aberto}>\n'
            f'        <summary>{p}</summary>\n'
            f'        <div class="faq-answer"><p>{r}</p></div>\n'
            f'      </details>'
        )
    return (
        '<section class="faq-section" id="faq">\n'
        '  <div class="wrap">\n'
        '    <div class="sec-head">\n'
        '      <div class="eyebrow">Perguntas Frequentes</div>\n'
        '      <h2>O que os leitores costumam perguntar</h2>\n'
        '      <div class="divider"></div>\n'
        '      <p>Por onde começar, o que é fato e o que é ficção, e onde encontrar cada obra.</p>\n'
        '    </div>\n'
        '    <div class="faq-list">\n'
        + "\n".join(itens) + "\n"
        '    </div>\n'
        '  </div>\n'
        '</section>\n\n'
    )


html = INDEX.read_text(encoding="utf-8")

if 'id="faq"' in html:
    print("Secao FAQ ja existe na home. Nada a fazer.")
    sys.exit(0)

if "faq-section" not in html:
    html = html.replace("</style>", CSS + "</style>", 1)

ancora = '<section class="contact-section" id="contato">'
if ancora not in html:
    sys.exit("ERRO: nao achei a secao de contato para ancorar a FAQ")
html = html.replace(ancora, montar_html() + ancora, 1)

if "--dry-run" in sys.argv:
    print("(dry-run) CSS e secao FAQ seriam inseridos.")
else:
    INDEX.write_text(html, encoding="utf-8")
    print(f"FAQ inserida na home: {len(PERGUNTAS)} perguntas, antes da secao de contato.")
