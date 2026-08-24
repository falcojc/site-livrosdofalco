# LP /romance-historico · Design

Data: 24/08/2026
Status: **aprovado pelo Julio em 24/08**, pronto para virar plano de implementação
Rota: `/romance-historico/`
Prazo: sobe assim que ficar pronta. Referências de calendário: promoção 31/08, Bienal 07/09

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

### 2.4. Calendário de promoção, fechado em 24/08

O KDP Select dá, por período de 90 dias e **por título**, uma escolha entre Promoção de
Livro Grátis (até **5 dias**) ou Oferta Relâmpago (até 7 dias, desconto e não grátis). As
duas são mutuamente exclusivas no mesmo ciclo, e **a Oferta Relâmpago não existe na
`amazon.com.br`**: ela só roda em `amazon.com` e `amazon.co.uk`. No Brasil, a única
ferramenta disponível é a promoção grátis de 5 dias.

Como o ciclo é por título e não por conta, dois títulos cobrem dois objetivos que um só não
cobriria:

| Título | Janela | Dias | Serve para |
|---|---|---|---|
| **A Saga Italiana** | 31/08 (seg) a 04/09 (sex) | 5 | Colher avaliação e gerar número antes das reuniões com editoras |
| **O Siciliano** | 05/09 (sáb) a 09/09 (qua) | 5 | Cobrir o dia da Bienal (07/09) e ser o que o Julio aponta na feira |

Ao agendar no KDP, **a data de término é exclusiva**: para a Saga terminar em 04/09, digitar
05/09. Conferir antes o ciclo de Select de cada título, porque dias não usados evaporam na
virada do período, e os dois títulos entraram no Select em datas diferentes (a Saga em
agosto de 2026, O Siciliano desde 2024).

O Siciliano grátis na feira também deixa a value ladder redonda: pega grátis, gosta, sobe
para o omnibus a R$ 19,90. E ele é a única obra do catálogo com 4,0★, então avaliação nova
ali compõe sobre o que já existe em vez de começar do zero.

**O objetivo da promoção é avaliação, não receita** (grátis não paga royalty). Se a página,
o post e o e-mail terminarem em "baixe grátis" em vez de "baixe e, se gostar, avalie", o
único ativo de prova social construível sem dinheiro é queimado.

**Consequência para a página:** a seção do degrau de ticket precisa de dois estados, e ao
contrário do que a v1 deste spec dizia, **o estado de promoção vai ser usado**, duas vezes,
já na primeira quinzena de vida da página.

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

**Auditoria do site feita em 24/08, atrás dessa mesma família de erro.** O site está limpo
de "Etna", de "mais vendido" e de contagem de páginas inflada, e a home descreve O Siciliano
como "Sicília, 1880 › os cafezais brasileiros", que é preciso sem se comprometer com a
cidade errada. **Dois erros reais estavam publicados no blog e foram corrigidos:**

| Arquivo | Era | Virou |
|---|---|---|
| `blog/posts/guerra-secessao-corrida-ouro-justica.md` | "a **aclamada** obra Sangue Frio" | "o **romance histórico** Sangue Frio" |
| `blog/posts/revolucao-do-conteiner-porto-genova.md` | "O Comandante, **obra-prima** do autor" | "O Comandante, **romance** de Domenico Falco" |

Sangue Frio e O Comandante têm **zero avaliações** na Amazon. "Aclamada" e "obra-prima" são
prova social que não existe, escritas em material publicado. A troca por "romance histórico"
no primeiro caso ainda devolve o bigrama da keyword de maior volume da conta para dentro de
um post indexado.

### 2.6. Por que a porta 3 é Amor e Ódio, e não O Asilo

O Asilo era a escolha inicial, com o plano de reenquadrá-lo de "suspense psicológico" para
"nazista foragido no Brasil dos anos 1950". **O reenquadramento não resolve o problema, e o
motivo é que a LP não controla a loja.** A sinopse oficial na Amazon diz, com estas
palavras: *"Um thriller psicológico de tirar o fôlego disfarçado de um tranquilo lar para
idosos."* O leitor clica na ficha, chega na PDP e lê "thriller psicológico".

Isso cria uma **contradição interna**: a seção 4 desta página define romance histórico por
oposição ao passado usado como cenário, e a loja desmente a definição dois cliques depois.
Numa página cuja autoridade depende justamente dessa definição (é o bloco que a IA cita), a
contradição custa mais do que a obra rende.

O segundo motivo é o H1. Comparando as sinopses oficiais:

- **Amor e Ódio:** *"Famílias da Andaluzia dilaceradas pelo poder e escolhas implacáveis
  durante a ascensão de um ditador."*
- **O Asilo:** *"criminosos nazistas, fraudes e fantasmas."*

O H1 da página é "até onde você iria pela sua família, e o que essa escolha lhe custaria".
Uma das duas é esse H1 em forma de livro. A outra não menciona família.

| | O Asilo | Amor e Ódio |
|---|---|---|
| Encaixe no H1 | não aparece | é a própria sinopse |
| Romance histórico sem asterisco? | não, a loja chama de thriller | sim |
| Keyword tier A | "suspense psicológico brasileiro" (outro gênero) | "segunda guerra mundial ficção" |
| Persona mulher 35+ | thriller de asilo | paixão proibida em tempo de guerra |
| Páginas | 122 | **87** |

**O que se perde com a troca, registrado de propósito:** substância (87 páginas contra 122,
a mais curta do trio, num gênero de calhamaço) e território ("nazista foragido no Brasil" é
o gancho mais raro do catálogo, enquanto Guerra Civil Espanhola é a avenida mais lotada do
gênero). O segundo argumento foi pesado e descartado: competição de categoria decide BSR e
also-bought na Amazon, não decide qual ficha converte dentro da própria LP, onde o visitante
escolhe entre três livros do mesmo autor.

O Asilo não sai do site. Continua em `/categoria/submundo-traicoes-misterios/`.

---

## 3. Decisões tomadas

| Decisão | Escolha | Motivo |
|---|---|---|
| Ação principal | Captura de e-mail (audiolivro de O Comandante) | Única conversão que o site já produziu. Alimenta a lista que pede avaliação |
| Amazon | Saída secundária, nas fichas | 57 e 68 cliques já converteram 0% |
| Eixo das portas | Perfil de leitor, com sobrelinha de ambientação | Decisão do Julio. A sobrelinha compensa o custo de autoclassificação num tráfego de 4s |
| As 3 obras | O Siciliano · O Mestre das Tormentas · Amor e Ódio | Amor e Ódio entrou no lugar de O Asilo em 24/08, ver 2.6 |
| Saga Italiana | Seção própria, degrau de ticket, não porta | Se o omnibus vira porta, o degrau morre: não sobra para onde subir |
| Selo de estrelas | Não, na v1 | 1 avaliação por obra. Reavaliar depois da colheita da promoção |
| Definição do gênero | Desce para depois das portas | Obstáculo para o pago de 4s. Indiferente para a IA, que lê a página inteira |
| Tag de afiliado | Sim, `falcojc-20` mais `ascsubtag` | Padrão do site. Divulgação já está no rodapé desde 16/08 |
| Data de publicação | Sobe assim que ficar pronta, sem esperar avaliação | Assimetria de reversibilidade: o selo de estrelas entra depois com um edit de uma linha, o tempo de indexação no Search Console não se recupera. A página precisa já estar indexada quando a promoção rodar (31/08) e na Bienal (07/09) |
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

**Andaluzia, anos 1930** · *O Amor em Tempo de Guerra* · **Amor e Ódio**
> Uma paixão proibida em famílias que a Guerra Civil Espanhola vai dilacerar. Enquanto um
> ditador sobe ao poder, cada escolha custa alguém, e ninguém escolhe sem pagar.

Fontes: `catalogo.json` (O Siciliano, Amor e Ódio), PDP publicada `/o-mestre-das-tormentas`
(John Storm, texto já validado), ficha do KDP do omnibus (Vassouras).

Com essa composição a vitrine cobre **família e imigração, aventura e mar, amor e guerra**,
que é recorte melhor para a persona medida (mulher 35+) do que família, mar e thriller.

### Seção 3 · A Saga Italiana, degrau de ticket

Três romances completos num volume só, cobrindo quase um século da diáspora italiana:

- **Os Dois Irmãos** · Campânia a Mendoza, a partir de 1860
- **O Siciliano** · Sicília e Brasil, 1880 a 1943
- **Os Italianos** · Calábria, Nova York e São Paulo, 1892 ao século XXI

Conteúdo inédito: prefácio do autor, linha do tempo que encaixa as três histórias no mesmo
século, comparação entre as três famílias.

Ancoragem: **R$ 29,70 comprados avulsos (3 × R$ 9,90), R$ 19,90 na edição especial.**

**Dois estados, e os dois vão ser usados já na primeira quinzena** (ver 2.4). O estado de
promoção precisa ser uma troca de uma linha, não uma reescrita, porque ele liga e desliga
quatro vezes em dez dias:

| Data | Estado | Título grátis |
|---|---|---|
| até 30/08 | normal | |
| 31/08 a 04/09 | promoção | A Saga Italiana (esta seção) |
| 05 a 09/09 | promoção | O Siciliano (a porta 1, seção 2) |
| a partir de 10/09 | normal | |

- *Estado normal:* CTA `Quero a Edição Especial`, com a ancoragem de preço (R$ 29,70 avulsos
  contra R$ 19,90).
- *Estado de promoção:* selo "grátis até \<data\>", e o CTA vira `Baixar grátis e, se
  gostar, avaliar`. **O pedido de avaliação é parte do CTA, não um rodapé.**

Note que a segunda janela liga o estado de promoção na **porta 1** (O Siciliano), não nesta
seção. A implementação precisa suportar o selo nos dois lugares.

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

## 5. O terceiro público: Bienal do Livro, 07/09

Até aqui a página tinha dois públicos: tráfego pago de busca e orgânico. A Bienal cria um
terceiro, com comportamento diferente dos dois: **pessoa de pé no Anhembi, celular na mão,
que acabou de conversar com o Julio.**

**Dimensionamento: nenhum.** É o primeiro evento, sem stand, só circulação e boca a boca.
Não há base para estimar leads, e a página não deve ser redesenhada em cima de um número
que não existe. A Bienal **ganha uma porta de entrada na página, não um redesenho dela.**

**O QR aponta para a LP, não para a Amazon.** Se ele levasse direto à loja, o evento não
deixaria nada: sem e-mail, sem medição própria e com o clique dissolvido num relatório de
afiliado que já mostrou 68 cliques e 0 pedidos. Apontando para a LP, a conversa presencial
vira lead, e a Amazon continua a um clique de distância dentro da página.

**URL do QR:**
`https://www.livrosdofalco.com.br/romance-historico/?utm_source=bienal&utm_medium=qrcode&utm_campaign=bienal2026`

Sem UTM, o tráfego da feira entra no GA4 como direto e se mistura com o resto, e não há como
saber o que o evento rendeu.

**A arte salva na galeria de fotos do celular é a decisão certa** (rede do Anhembi em dia de
Bienal é péssima) e resolve o problema de *mostrar* o QR. Mas ela não resolve o do outro
lado: quem escaneia ainda depende da própria rede para abrir a página. Duas consequências de
projeto:

1. O peso da página deixa de ser desejável e vira requisito. Reforça o padrão `/arquetipos`
   e mata qualquer ideia de vídeo nesta LP.
2. **A LP precisa funcionar como destino frio.** Em feira é normal a pessoa escanear, o
   celular guardar o link e ela abrir só à noite, em casa, fora do contexto da conversa. A
   página não pode pressupor que o visitante lembra quem é Domenico Falco.

### Sobre o promocode "Bienal10off"

**Não é possível, e não é limitação do plano: é limitação da plataforma.** O KDP não oferece
cupom nem código promocional para autor de eBook (cupons existem no Seller Central, para
produto físico, que é outro programa). E a Oferta Relâmpago, que seria o mecanismo de
desconto mais próximo, **não existe na `amazon.com.br`**: roda só em `amazon.com` e
`amazon.co.uk`.

**A boa notícia é que o desconto da Bienal já existe e é maior que 10%: é 100%.** O Siciliano
estará grátis de 05 a 09/09, e o dia 07/09 cai dentro. Quem o Julio encontrar na feira pega
o livro de graça, sem código, sem fricção e sem depender de nada além do QR. O material
impresso deve dizer exatamente isso.

Se em algum momento fizer sentido dar algo que **só** o público da feira tem, o lugar é o
site, não a Amazon, porque ali o Julio controla a entrega. Fora do escopo desta v1.

---

## 6. SEO e técnico

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
  Amor e Ódio `B0D8RTCPNP`, A Saga Italiana `B0HFPS4K6R` (conferido no JSON-LD da home).
- **URL longa, não link curto:** o `analytics.js` extrai o ASIN do padrão `/dp/XXXXXXXXXX`,
  e link curto chega ao GA4 como `(sem asin)`.

**Menu:** o menu principal não aguenta mais item (8px de folga em 1280px). A ligação ao
resto do site é pelo rodapé e pelo sitemap, igual à `/arquetipos`.

---

## 7. O que fica de fora, de propósito

- **Selo de estrelas e contagem de avaliações.** Ver 2.1. Reavaliar na v2.
- **Grade com as 30 obras.** É o que a página existe para não ser.
- **Os Templários**, em qualquer papel. 2,7★ com 66% das notas em 1 e 2, fora de conteúdo e
  de promoção até a média subir.
- **O Asilo**, como porta de entrada. Ver 2.6. Continua vivo em
  `/categoria/submundo-traicoes-misterios/`.
- **Adjetivo de prova social** em qualquer lugar da página: "aclamado", "obra-prima",
  "sucesso", "mais vendido". Com 5 avaliações no catálogo inteiro, nenhum deles é
  verificável, e dois já tiveram que ser removidos do blog em 24/08.
- **Link para a `/audiolivro`.** Ela é captura pura, sem link de saída. Esta página tem a
  mesma oferta embutida, então mandar para lá seria um salto desnecessário.
- **Vídeo.** Peso sem função nesta página.

---

## 8. Riscos, e o que reavaliar depois

| Risco | Sinal de que aconteceu | O que fazer |
|---|---|---|
| Perfil de leitor exige autoclassificação, e o pago fica 4s | Taxa de clique nas três fichas fica achatada e igual | Testar troca dos rótulos de perfil por cenário histórico puro |
| A página não fica pronta antes de 31/08 e perde a janela de indexação | Search Console sem a URL quando a promoção começa | Publicar mesmo incompleta é preferível a publicar tarde: o que falta entra por edição, o tempo de indexação não volta |
| Bienal não gera volume nenhum | Zero sessões com `utm_source=bienal` em 07/09 | Custo já é baixo (uma arte e um QR). Não redesenhar a página em cima disso, ver seção 5 |
| A promoção não gera avaliação | Contagem de avaliações não sobe até 05/09 | A v2 não ganha selo, e a prova social tem que vir de outro lugar (Skoob, grupos de Kindle) |
| Amor e Ódio é curto demais para o gênero (87p) | Porta 3 recebe clique e a PDP não segura | Trocar por A Vila (101p, 5,0★, ancora "segunda guerra mundial romance", tier A), aceitando que ela se aproxima do tema da porta 1 |
| Conversão continua 0% na PDP | Leads sobem, vendas seguem em zero | Confirma que o gargalo é a PDP, não o site. Nada na LP resolve isso |

**O que esta página não resolve, e é importante estar escrito:** a PDP da Amazon converte
0%. A LP pode melhorar qualidade de tráfego, custo por clique, orgânico e captura. Ela não
faz a página do produto vender. A alavanca continua sendo avaliação.
