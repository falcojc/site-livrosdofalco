# LP /audiolivro · Design

Data: 17/08/2026
Status: aprovado por Julio, pronto para virar plano de implementação

---

## 1. Por que esta página existe

O diagnóstico do funil (ago/2026) mostrou o gargalo real: **43 pessoas clicaram para a
Amazon e 0 deixaram e-mail**. Ir à loja tem mais atrito que preencher um formulário, então
o problema nunca foi fricção. Era ausência de oferta: o site pedia e-mail sem entregar
nada em troca.

O plano de growth escolheu como isca o audiolivro de O Comandante, com o argumento de que
a amostra de texto não serve porque a Amazon já a dá de graça, e pedir e-mail por algo
livre é oferecer um negócio pior que o status quo.

**Esse mesmo argumento derruba a versão original da isca.** O audiolivro completo já está
público no YouTube, no canal `@livrosdofalco`, sem cadastro. Quem chegasse na LP e lesse
"deixe seu e-mail e receba o audiolivro completo" acharia o mesmo áudio em dez segundos.

**A isca, então, não é o conteúdo: é o formato.** O que a LP entrega e o YouTube não:
arquivos MP3 para baixar, separados por capítulo, que tocam offline no carro, na cozinha
ou na caminhada, sem anúncio, sem depender de sinal e sem precisar olhar para a tela. Isso
é verdadeiro, é verificável e fala diretamente com a persona real do LdF, que é mulher 35+
e ouve enquanto faz outra coisa.

Isso preserva o vídeo do YouTube, que é ativo em construção, em vez de destruí-lo para
criar escassez artificial.

---

## 2. Decisões tomadas

| Decisão | Escolha | Motivo |
|---|---|---|
| O que é a isca | O formato (MP3 offline por capítulo), não o conteúdo | O conteúdo já é livre no YouTube |
| CTA da Amazon na LP | Não. Só na página de obrigado | Uma página, um objetivo. A venda muda de lugar, não desaparece |
| Escopo | Só a LP. A captura no ponto de saída fica para spec próprio | Ela mexe no clique de saída, que é o único comportamento vivo do funil, e precisa ser testada sozinha |
| Lista da Brevo | Lista nova, separada, só da LP | Segmentação limpa: dá para medir a LP sem contaminar a lista de leitores do site |
| Double opt-in | Mantido na lista, mas a entrega não depende dele | Entrega imediata na página de obrigado, lista continua limpa |

---

## 3. Escopo

**Entra:**
- Página `/audiolivro`, de captura, sem links de saída.
- Página `/audiolivro/obrigado`, de entrega e venda.
- Os 22 capítulos reencodados, mais o pacote único para baixar tudo.
- Um evento de conversão já reconhecido pelo Google Ads.

**Não entra, de propósito:**
- Banco de dados. A Brevo guarda o contato, o site não guarda nada.
- Contador de download, área de membros, login.
- Teste A/B no lançamento. Sem volume, teste A/B não conclui nada.
- A segunda porta de captura (ponto de saída para a Amazon).
- Qualquer prova social por avaliação. São 5 avaliações no catálogo e a média real é
  3,4 estrelas: exibir enfraquece e inventar está fora de questão.

---

## 4. Arquitetura

```
audiolivro/
  index.html            página de captura (formulário nativo Brevo)
  obrigado/
    index.html          entrega + CTA Amazon
audio/
  o-comandante-amostra.mp3          (já existe no repo)
  o-comandante/
    01-lembrancas.mp3 ... 22-epilogo.mp3
    o-comandante-audiolivro.zip
```

Padrão idêntico ao de `/newsletter`, que já roda em produção: HTML estático, sem
framework, `<script src="/analytics.js">` no topo (regra permanente do projeto, nunca
copiar o snippet do gtag solto).

**Fluxo:**

1. Visitante chega em `/audiolivro`, ouve a amostra, preenche nome e e-mail, aceita o
   opt-in.
2. O formulário posta direto para a Brevo (`sibforms.com`), com o script da própria Brevo
   cuidando de validação e estado do botão, sem código nosso no caminho e sem passar pelo
   Supabase.
3. A Brevo grava o contato na lista nova, dispara o e-mail de confirmação (double opt-in) e
   redireciona o navegador para `/audiolivro/obrigado`.
4. A página de obrigado entrega os arquivos na hora, avisa para confirmar o e-mail e
   oferece a compra na Amazon.

**Por que a entrega não espera a confirmação:** entre 20% e 40% das pessoas nunca voltam
ao inbox para confirmar. Se o arquivo dependesse disso, a promessa "receba agora" viraria
"vá procurar seu e-mail", e a LP perderia justamente na última etapa. Quem não confirmar
levou o áudio e não entra na newsletter, que é exatamente o filtro desejado.

---

## 5. Conteúdo da página de captura

Ordem pensada para 4 segundos de atenção, que é a média do tráfego pago hoje.

**Bloco 1, acima da dobra no desktop e no celular:** promessa, subtítulo e o formulário
visível sem rolar.

> **Recomendado**
> H1: *O audiolivro de O Comandante, completo, no seu celular*
> Apoio: *1h55 de narração em 22 capítulos, para baixar e ouvir offline: no carro, na
> cozinha, na caminhada. Sem anúncio e sem precisar olhar para a tela.*

> **Alternativa, mais dramática e menos concreta**
> H1: *Ele perdeu tudo na guerra e construiu um império nos mares*
> Apoio: mesmo texto acima.

A recomendada ganha porque o diferencial da oferta é o formato, e a alternativa compete de
frente com o título do vídeo do YouTube, que entrega a mesma promessa de graça.

**Bloco 2: player com a amostra real** (`/audio/o-comandante-amostra.mp3`, 2,8MB, já no
repo). Prova antes do pedido: ela ouve a voz antes de decidir se quer. Reaproveita o
componente e o evento `play_audiobook_sample` que já existem.

**Bloco 3: o que você recebe**, concreto e sem adjetivo: 22 capítulos, 1h55 de narração,
arquivos MP3 de cerca de 2,4MB, tocam em qualquer celular, computador ou carro.

**Bloco 4: uma linha sobre o autor**, com a foto que já está no repo
(`author-domenico-falco.jpg`): 30 romances publicados. Volume de obra é a prova honesta
disponível.

**Cabeçalho e rodapé:** logo sem link, e uma linha só de rodapé com privacidade e contato.
Nenhum menu, nenhuma navegação, nenhum link para fora. A página tem um caminho: o
formulário.

**Aviso de privacidade** junto do botão, curto, com o opt-in desmarcado por padrão, igual
ao formulário que já está em produção.

---

## 6. Página de obrigado

Nesta ordem, que importa:

1. **Confirmação e entrega imediata.** Botão principal "Baixar o audiolivro completo"
   (pacote único) e, abaixo, a lista dos 22 capítulos, cada um com play e download
   individual.
2. **Aviso do double opt-in:** "confirme no e-mail que acabamos de enviar para continuar
   recebendo as novidades". Aviso, não obstáculo: o download já está liberado acima.
3. **Só então a Amazon.** "Prefere ler? O Comandante está na Amazon", com o link de
   afiliado `https://link.amazon/B02BbXrEH`. Este é o pico de reciprocidade e de interesse:
   ela acabou de receber 1h55 de narração.

O link no padrão `link.amazon` já dispara `click_to_amazon` sozinho, porque o listener
casa por hostname. Nenhum código novo é necessário para medir a saída.

---

## 7. Pipeline dos arquivos de áudio

Origem: `2. Produto/Catalogo/Obras Literárias/30. O Comandante/4. Audiobook/Capitulos/`,
22 arquivos, 159MB, gravados em 192kbps estéreo a 44,1kHz.

**192kbps estéreo é desperdício para voz narrada.** O padrão de audiolivro é 64kbps mono,
que para narração é indistinguível na prática e derruba o peso em cerca de dois terços:
159MB viram aproximadamente 53MB, cerca de 2,4MB por capítulo. Nesse tamanho os arquivos
cabem no próprio repositório e são servidos pelo CDN da Vercel, sem Google Drive, sem
Supabase Storage e sem custo nenhum.

Cada arquivo sai com:
- nome numerado e sem acento (`01-lembrancas.mp3`), para ordenar certo no player do celular;
- tags ID3 (título com número do capítulo, autor, álbum, número da faixa);
- a capa de `covers/o-comandante.jpg` embutida, para o app mostrar a arte.

O script de lote fica em `.claude/audiolivro/prepara_audio.py`, seguindo a regra do projeto
de manter ferramenta minha fora das pastas de material do Falco, e deve derivar os caminhos
em vez de hardcodar, porque a árvore de pastas muda.

**Custo no repositório, declarado:** os 22 capítulos somam cerca de 53MB e o pacote único
para baixar tudo repete o mesmo conteúdo, então o repositório cresce cerca de 106MB. Isso é
tranquilo para o GitHub e para a Vercel, mas é bom saber que o número dobra por causa do
pacote. Se preferir enxugar, dá para servir só os capítulos individuais e cortar o pacote,
ao custo de a promessa "baixar tudo com um clique" virar 22 cliques, o que enfraquece a
oferta. A recomendação é manter o pacote.

---

## 8. Medição

**Evento de conversão: `generate_lead`**, com `event_label: 'audiolivro'`, disparado no
carregamento da página de obrigado.

Reaproveitar esse nome em vez de criar um evento novo é decisão deliberada: `generate_lead`
já está ligado à conversão do Google Ads pela regra `ads_conversion_Enviar_formul_rio_de_le_1`
do GA4. A LP nasce medindo, e você não precisa criar meta nova no painel do Ads nem esperar
as 48h de validação.

Também medidos, sem código novo: `play_audiobook_sample` (amostra ouvida na LP) e
`click_to_amazon` (saída na página de obrigado).

Leitura correta do funil da LP: `page_view` em `/audiolivro` → `play_audiobook_sample` →
`generate_lead` → `click_to_amazon`.

---

## 9. Pré-requisitos que dependem de você

A implementação trava sem isto, porque eu não tenho acesso ao painel da Brevo:

1. **Criar a lista.** Brevo → Contatos → Listas → Criar: `Leitores — Audiolivro`.
2. **Criar o formulário.** Brevo → Formulários → Criar, com três campos: `EMAIL`,
   `JOB_TITLE` (é o campo do nome; a Brevo não oferece um atributo `NOME` nesta conta, e o
   nome vive tecnicamente em `JOB_TITLE`) e `OPT_IN` como checkbox obrigatório e desmarcado
   por padrão, que é o que a LGPD pede.
3. **Vincular à lista nova** e manter o double opt-in ligado.
4. **Configurar o redirecionamento** pós-envio para
   `https://www.livrosdofalco.com.br/audiolivro/obrigado/`. É isso que faz a entrega
   acontecer sem depender do e-mail de confirmação. Se a Brevo não oferecer redirect neste
   plano, o plano B é interceptar o submit no JavaScript, o que funciona mas adiciona uma
   peça que pode quebrar em silêncio, como já aconteceu antes com o `<svg>` de loading do
   botão da Brevo.
5. **Me passar a action URL** do formulário novo (o endereço `https://<id>.sibforms.com/serve/...`).

**Pendência herdada, não bloqueia:** os capítulos 18 e 21 estão os dois nomeados "Silêncio"
nos arquivos de origem. Se for intencional, o nome sai repetido na lista da página de
obrigado, o que é estranho mas inofensivo. Se for engano, vale corrigir antes de gerar os
arquivos, porque o nome entra na tag ID3 e no nome do arquivo.

---

## 10. Riscos declarados

**A LP não cria tráfego.** São cerca de 197 visitantes orgânicos por mês. Mesmo uma
conversão excelente de 10% dá vinte e-mails mensais. A página existe para que a mídia paga
prevista no plano tenha um destino decente e para que o teste de conteúdo de 4 semanas
tenha para onde mandar gente. Julgar a LP por volume de leads no primeiro mês, sem mídia
rodando, produz a leitura errada e pode matar uma peça que está funcionando.

**A régua certa no primeiro mês é taxa, não volume:** visitantes de `/audiolivro` que
viram lead. Abaixo de 5% o problema é a página; acima de 15% o problema é só falta de
tráfego.

**O YouTube continua entregando o mesmo áudio de graça.** Toda a razão de existir da LP
está na clareza de que ali se baixa e no YouTube se assiste. Se o texto da página não
deixar isso evidente na primeira linha, a página não tem motivo para existir.

---

## 11. Critérios de aceite

1. `/audiolivro` carrega sem nenhum link que leve para fora da página, incluindo header e
   rodapé.
2. O formulário grava o contato na lista nova da Brevo e o navegador chega em
   `/audiolivro/obrigado`.
3. A página de obrigado entrega o download sem exigir a confirmação do e-mail.
4. Os 22 arquivos tocam com nome e capa corretos num celular real, na ordem certa.
5. `generate_lead` com rótulo `audiolivro` aparece no DebugView do GA4.
6. O download completo que a pessoa recebe fica abaixo de 60MB (os 22 capítulos somados).
7. Lighthouse mobile de performance acima de 90 na página de captura, que é a que recebe
   tráfego pago.
