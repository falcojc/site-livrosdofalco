# LP /romance-historico · Design

Data: 24/08/2026
Status: aguardando revisão do Julio
Rota: `/romance-historico/`

---

## 1. Por que esta página existe

"Romance histórico" é a palavra-chave de maior volume da campanha de Pesquisa do LdF. Hoje
ela aponta para a home com o fragmento `#obras`, e o Google Ads avalia a URL sem o
fragmento, ou seja, ele julga a home inteira: 138 KB de HTML, título genérico e trinta
capas. O hub `/categoria/` também não serve como destino (title "Categorias", H1
"Categorias", zero ocorrências do bigrama "romance histórico", 2.194 impressões a 1,28% de
CTR).

Uma página própria resolve três problemas com um artefato só:

1. **Orgânico.** 7 de 36 páginas do site estão indexadas. Uma página cujo title, H1 e
   conteúdo casam com um termo de busca real é candidata a ranquear.
2. **Citação em IA.** A medição de descoberta deu 0/9. Uma página que define o gênero e
   comenta obras é exatamente o formato que ChatGPT e Perplexity citam.
3. **Ads.** O destino melhor vem como efeito colateral, não como motivo.

O argumento não é o Ads. Se fosse só campanha, a decisão racional seria pausar a keyword e
economizar os R$ 40,94, porque ela não converte.

**A tese que governa a página: ela não pode ser catálogo.** Catálogo já existe em
`/categoria/` e não converte. Esta página responde a pergunta de quem digita "romance
histórico" no Google, que é: *que livro eu leio?*

---

## 2. O que os dados disseram, e o que isso mudou

### 2.1. Não existe "as 3 obras com melhor lastro"

Medição na loja em 24/08/2026 (busca do autor em `amazon.com.br`, 32 resultados):

| Obra | Nota | Nº de avaliações |
|---|---|---|
| A Vila | 5,0★ | 1 |
| O Siciliano | 4,0★ | 1 |
| Os Templários | 2,7★ | 3 (passivo, fora de tudo) |
| as outras 28 | sem nota | 0 |

Cinco avaliações no catálogo inteiro, em três obras. Duas com nota positiva, um voto cada.

**Consequência de copy, não só de escolha: selo de estrelas está proibido nesta página.**
Exibir "4,0★" ao lado de "(1 avaliação)" sublinha a ausência de prova social na página que
precisa vender. Exibir "4,0★" sem o número é enganoso, e a Amazon mostra o "(1)" dois
cliques adiante.

### 2.2. "Popularidade" do catálogo é número fantasma

A coluna do Catálogo Mestre se chama, literalmente, `Popularidade (rank do CSV)`. Ordenando
as 31 obras por ela, o resultado é cronologia reversa quase perfeita (tudo de 2024 no topo,
2019 e 2020 no fundo). É ordem de listagem herdada, não venda. Somado a KENP = 0 e vendas =
0 no período medido, **não existe obra "mais popular" mensurada no catálogo.**

Proibido em qualquer material: "a obra nº 1 de popularidade", "Pop Rank #8" ou variação.

### 2.3. O CTA principal não pode ser a Amazon

Duas medições independentes:

- GA4, 23/07 a 23/08: **57 cliques do site para a Amazon → 0 vendas, 2 páginas de KENP.**
- Amazon Associates, 17/07 a 15/08: **68 cliques → 0 pedidos, R$ 0,00.**

A única conversão que o site já produziu foi lead: 3, a R$ 34,27 cada. Mandar a keyword
mais cara da conta para o destino que converteu 0% duas vezes é repetir o experimento
esperando outro resultado.

**Decisão: a captura de e-mail é a ação principal da página. A Amazon é a saída secundária,
para quem já decidiu.**

### 2.4. A Saga Italiana estará grátis de 26 a 30/08

A ficha do KDP é explícita: o omnibus foi montado *para* a promoção grátis de 26 a 30/08. O
produto que a seção do degrau de ticket vende a R$ 19,90 custa R$ 0,00 nessa janela. A seção
precisa de dois estados.

O objetivo da promoção é **avaliação**, não receita (grátis não paga royalty). Se a página,
o post e o e-mail terminarem em "baixe grátis" em vez de "baixe e, se gostar, avalie", o
único ativo de prova social construível sem dinheiro é queimado.

### 2.5. Seis erros factuais no rascunho de origem, que não podem entrar na página

| No rascunho | O que os arquivos dizem |
|---|---|
| "O Siciliano, obra nº 1 de popularidade" | Rank do CSV, ordem de listagem herdada |
| "fugindo das encostas do vulcão Etna" | Disputa de terras que lhe custa o pai. Etna não aparece em fonte nenhuma |
| "lavouras de café de São Paulo" | **Vassouras, no Rio de Janeiro.** São Paulo vem depois |
| "O Asilo, Pop Rank #8" | Mesmo rank fantasma |
| "O Mestre das Tormentas, aclamada pela riqueza de mapas e táticas navais" | Zero avaliações. Não há aclamação a citar |
| "Atraessar o Oceano com Matteo" | Typo no CTA |

O erro de Vassouras é da mesma família que a v1 da descrição do KDP cometeu e foi corrigida
em 18/08. **Regra desta página: nenhum detalhe de enredo entra sem sair de
`.claude/catalogo.json`, da ficha do KDP (`Relatórios/ficha-kdp-a-saga-italiana-17-08-2026.md`)
ou de uma PDP já publicada.**

### 2.6. O Asilo não é thriller psicológico, é nazista foragido no Brasil

Sinopse oficial: *"Por trás das paredes de um asilo, escondem-se criminosos nazistas,
fraudes e fantasmas."*

Vendido como "suspense psicológico", ele desalinha com quem buscou romance histórico.
Vendido como o que aconteceu com os nazistas que fugiram para a América do Sul, ele é
romance histórico de linhagem conhecida e com demanda própria. Muda o enquadramento, não a
obra.

---

## 3. Decisões tomadas

| Decisão | Escolha | Motivo |
|---|---|---|
| Ação principal | Captura de e-mail (audiolivro de O Comandante) | Única conversão que o site já produziu. Alimenta a lista que pede avaliação |
| Amazon | Saída secundária, nas fichas | 57 e 68 cliques já converteram 0% |
| Eixo das portas | Perfil de leitor, com sobrelinha de ambientação | Decisão do Julio. A sobrelinha compensa o custo de autoclassificação num tráfego de 4s |
| As 3 obras | O Siciliano · O Mestre das Tormentas · O Asilo | Decisão do Julio |
| Saga Italiana | Seção própria, degrau de ticket, não porta | Se o omnibus vira porta, o degrau morre: não sobra para onde subir |
| Selo de estrelas | Não, na v1 | 1 avaliação por obra. Reavaliar depois da colheita da promoção |
| Definição do gênero | Desce para depois das portas | Obstáculo para o pago de 4s. Indiferente para a IA, que lê a página inteira |
| Tag de afiliado | Sim, `falcojc-20` mais `ascsubtag` | Padrão do site. Divulgação já está no rodapé desde 16/08 |
| Data de publicação | Sem data. Gatilho: quando a colheita de avaliações da promoção for medida | Decisão do Julio. O gatilho existe para a página não virar limbo |
| Enquanto ela não existe | Trocar a URL final do Ads de `#obras` para `/categoria/raizes-sacrificio-familia/` | Ganho parcial, custo zero, dois cliques no painel |

---

## 4. Arquitetura da página

| # | Seção | Função |
|---|---|---|
| 1 | Herói e captura | Prender, nomear o gênero, oferecer o audiolivro |
| 2 | As 3 portas de entrada | Responder "que livro eu leio?" |
| 3 | A Saga Italiana | Degrau de ticket, e âncora da promoção |
| 4 | O que é romance histórico, e o que não é | Corrigir expectativa, alimentar orgânico e IA |
| 5 | Captura, versão completa | Recuperar quem rolou até o fim |

### Seção 1 · Herói e captura

- **Sobrelinha:** `Romance histórico brasileiro · 30 obras de Domenico Falco`
- **H1:** *Até onde você iria pela sua família? E o que essa escolha lhe custaria?*
- **Subtítulo:** romances históricos de alta imersão, onde o passado não é cenário
  decorativo: é o que força pessoas comuns a decisões impossíveis.
- **CTA principal:** `Ouvir um romance completo, de graça` (rola para o formulário)
- **CTA secundário, texto simples:** `ou veja por onde começar a ler` (rola para as portas)

O H1 é emocional de propósito: é o tema único do autor, e é o que separa Domenico Falco de
Ken Follett (que trata o indivíduo como peça de um panorama geopolítico) e de García Márquez
(realismo mágico e solidão de linhagem). O bigrama literal "romance histórico" entra pela
sobrelinha, pelo title, pela meta description e pelo primeiro parágrafo, que é suficiente
para o Ads, que avalia a página inteira e não só o H1.

### Seção 2 · As 3 portas de entrada

Cada ficha, na ordem de leitura: **sobrelinha de ambientação** (o que o olho lê primeiro e
o que o Google indexa) → **rótulo de perfil** → **título da obra** → gancho de 2 a 3 linhas
→ link para a Amazon.

**Sicília e Brasil, 1880 a 1943** · *O Épico de Família* · **O Siciliano**
> Uma disputa de terras custa o pai de Matteo. Ele cruza o Atlântico e recomeça do zero nas
> fazendas de café de Vassouras, no Rio de Janeiro, antes de a família se mudar para São
> Paulo. Décadas depois, volta à Sicília para acertar o que deixou por resolver.

**Sete mares, a partir de 1700** · *A Aventura do Desconhecido* · **O Mestre das Tormentas**
> Filho de uma cozinheira, criado nos becos de Londres. Dado como morto num naufrágio no
> Pacífico Sul, ressurge nas águas asiáticas e atravessa a Rota da Seda atrás do único
> caminho de volta que ainda importa: para casa, e para quem ele deixou para trás.

**Brasil, anos 1950** · *O Suspense de Sombras* · **O Asilo**
> Atrás das paredes de um lar tranquilo para idosos, criminosos nazistas, fraudes e
> fantasmas. O que a Europa não julgou, o Brasil hospedou.

Fontes: `catalogo.json` (O Siciliano, O Asilo), PDP publicada `/o-mestre-das-tormentas`
(John Storm, texto já validado), ficha do KDP do omnibus (Vassouras).

### Seção 3 · A Saga Italiana, degrau de ticket

Três romances completos num volume só, cobrindo quase um século da diáspora italiana:

- **Os Dois Irmãos** · Campânia a Mendoza, a partir de 1860
- **O Siciliano** · Sicília e Brasil, 1880 a 1943
- **Os Italianos** · Calábria, Nova York e São Paulo, 1892 ao século XXI

Conteúdo inédito: prefácio do autor, linha do tempo que encaixa as três histórias no mesmo
século, comparação entre as três famílias.

Ancoragem: **R$ 29,70 comprados avulsos (3 × R$ 9,90), R$ 19,90 na edição especial.**

**Dois estados.** Como a página só entra depois da promoção de 26 a 30/08 (ver a decisão de
timing na seção 3), o estado "promoção ativa" **não serve para essa janela**: ele existe
para os ciclos seguintes, já que o KDP Select libera 5 dias grátis a cada 90 dias. A v1 nasce
no estado normal, com o estado de promoção construído e desligado, para ser ligado por
edição de uma linha quando o próximo ciclo for agendado.

- *Estado normal (v1, no ar):* CTA `Quero a Edição Especial`, com a ancoragem de preço.
- *Estado de promoção (construído, desligado):* selo "grátis até \<data\>", e o CTA vira
  `Baixar grátis e, se gostar, avaliar`. O pedido de avaliação é parte do CTA, não um
  rodapé.

Nota de conferência: a contagem de 417 páginas é a paginação do KDP, que é inflada (a
contagem por palavras dá ~295). Usar 417 na página é coerente com o que a loja mostra, mas
não usar esse número em material de análise interna.

### Seção 4 · O que é romance histórico, e o que não é

Existe para resolver o desalinhamento de quem busca "romance de época" esperando Bridgerton
e encontra drama de guerra. É também o bloco que Google e IAs citam.

Estrutura de duas colunas, com H2 literal `O que é romance histórico, e o que não é`:

- **Romance de época** usa o passado como cenário decorativo e idealizado: bailes, rituais
  de corte, trama romântica leve. O período é moldura.
- **Romance histórico** usa o passado como pressão. O período é o que força a escolha:
  guerra, fome, exílio, ocupação, perseguição. Nenhum personagem sai ileso.

Fechamento em uma linha, que é a frase mais citável da página: *"não escrevemos sobre bailes
de porcelana; escrevemos sobre o preço que se paga para manter os seus vivos."*

### Seção 5 · Captura, versão completa

Reaproveita a máquina da `/audiolivro`, que foi testada ponta a ponta em 21/08.

- **A isca é o formato, não o conteúdo.** O audiolivro de O Comandante já é público no
  YouTube sem cadastro. O que a LP entrega e o YouTube não: 23 faixas MP3 por capítulo, para
  baixar e ouvir offline, sem tela e sem anúncio. **Se essa distinção sair do texto, a
  oferta é pior que o status quo.**
- Números reais e conferidos: 1h51 de narração, 23 faixas, 56,7 MB no pacote.
- Formulário nativo da Brevo (nome e e-mail), sem os scripts da Brevo e do Google.
- **Captcha desligado** nesta página, igual à `/audiolivro`: com ele ligado no painel, a
  Brevo rejeita todo cadastro em formulário nativo, e o widget custaria 400 a 600 KB de JS
  numa página de tráfego pago. O campo-armadilha da própria Brevo continua filtrando bot.
- Mesma lista e mesma página de entrega `/audiolivro/obrigado`, com atributo de origem
  `ORIGEM = romance-historico` para segmentar sem duplicar a máquina.

**Gotcha a verificar na implementação:** o `generate_lead` da página de obrigado tem trava
de contagem dupla em `localStorage`. Com duas LPs alimentando a mesma página de entrega,
confirmar que a trava não suprime a conversão de quem já veio pela `/audiolivro`.

---

## 5. SEO e técnico

**Head**

- `<title>`: `Romance histórico: por onde começar · Domenico Falco` (52 caracteres)
- `meta description`: precisa conter o bigrama literal "romance histórico" e a promessa de
  escolha ("três portas de entrada"), não a lista de obras.
- Canonical própria, entrada no `sitemap.xml`, `index,follow`.

**JSON-LD**, seguindo o padrão já sincronizado no site:

- `FAQPage` com as perguntas que a seção 4 responde ("o que é romance histórico", "qual a
  diferença entre romance histórico e romance de época"). É o formato mais citado por IA.
- `ItemList` com as três obras, cada uma como `Book` (autor, ISBN ou ASIN, url).

**Performance**, herdando as decisões da `/arquetipos`:

- Alvo de peso na faixa da `/arquetipos` (52 KB de HTML), nunca da home (138 KB).
- Três capas apenas, com `srcset` e `width`/`height` **mais `height:auto`** (sem isso o
  atributo HTML vira o "usado" de `height` e o `aspect-ratio` é ignorado).
- Nenhuma `<img>` como filha comum de um `display:flex` que também centraliza outro
  conteúdo na mesma linha.
- `reveal` on scroll com rede de segurança de 2s além da classe `.js`, senão a página abre
  vazia em aba de segundo plano.
- Sem player de vídeo na v1. Se entrar depois, só em facade.

**Analytics**

- Fichas usam a classe `book-card`, para o `analytics.js` compartilhado capturar
  `click_to_amazon` sem tocar em código.
- Links de saída no padrão `amazon.com.br/dp/<ASIN>?tag=falcojc-20&ascsubtag=romance-historico-<obra>`.
- ASINs Kindle conferidos: O Siciliano `B0D9WS272F`, O Mestre das Tormentas `B08XYL4QZY`,
  O Asilo `B0DDHZZCS1`, A Saga Italiana `B0HFPS4K6R` (conferido no JSON-LD da home).
- **URL longa, não link curto:** o `analytics.js` extrai o ASIN do padrão `/dp/XXXXXXXXXX`,
  e link curto chega ao GA4 como `(sem asin)`.

**Menu:** o menu principal não aguenta mais item (8px de folga em 1280px). A ligação ao
resto do site é pelo rodapé e pelo sitemap, igual à `/arquetipos`.

---

## 6. O que fica de fora, de propósito

- **Selo de estrelas e contagem de avaliações.** Ver 2.1. Reavaliar na v2.
- **Grade com as 30 obras.** É o que a página existe para não ser.
- **Os Templários**, em qualquer papel. 2,7★ com 66% das notas em 1 e 2, fora de conteúdo e
  de promoção até a média subir.
- **Link para a `/audiolivro`.** Ela é captura pura, sem link de saída. Esta página tem a
  mesma oferta embutida, então mandar para lá seria um salto desnecessário.
- **Vídeo.** Peso sem função nesta página.

---

## 7. Riscos, e o que reavaliar depois

| Risco | Sinal de que aconteceu | O que fazer |
|---|---|---|
| Perfil de leitor exige autoclassificação, e o pago fica 4s | Taxa de clique nas três fichas fica achatada e igual | Testar troca dos rótulos de perfil por cenário histórico puro |
| Página sem data vira limbo | Passar a colheita da promoção sem a página existir | O gatilho combinado destrava: colheita medida, página entra |
| A promoção não gera avaliação | Contagem de avaliações não sobe até 05/09 | A v2 não ganha selo, e a prova social tem que vir de outro lugar (Skoob, grupos de Kindle) |
| O Asilo desalinha mesmo reposicionado | Cliques na porta 3 com rejeição alta na Amazon | Trocar por A Vila, que é 5,0★ e ancora "segunda guerra mundial romance", tier A |
| Conversão continua 0% na PDP | Leads sobem, vendas seguem em zero | Confirma que o gargalo é a PDP, não o site. Nada na LP resolve isso |

**O que esta página não resolve, e é importante estar escrito:** a PDP da Amazon converte
0%. A LP pode melhorar qualidade de tráfego, custo por clique, orgânico e captura. Ela não
faz a página do produto vender. A alavanca continua sendo avaliação.
