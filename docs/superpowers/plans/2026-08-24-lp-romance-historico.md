# LP /romance-historico · Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publicar `/romance-historico/`, uma landing page leve que intercepta a keyword de maior volume da conta de Ads e converte em lead de e-mail, com a Amazon como saída secundária.

**Architecture:** HTML estático único (`romance-historico/index.html`) com CSS em `<style>` inline, no mesmo padrão de `/arquetipos` e `/audiolivro`. O Eleventy copia a pasta inteira via `addPassthroughCopy`, sem passar pelo motor de template. Sem build step próprio, sem framework, sem dependência nova.

**Tech Stack:** HTML5, CSS inline, Eleventy 3.1.6 (só passthrough), formulário nativo da Brevo, `analytics.js` compartilhado, JSON-LD.

**Spec:** `docs/superpowers/specs/2026-08-24-lp-romance-historico-design.md`. Ler antes de começar. Em qualquer divergência entre este plano e o spec, **o spec manda**.

## Global Constraints

- **Idioma:** português do Brasil em todo texto visível.
- **Nunca usar travessão (—) em texto visível.** Usar vírgula, dois-pontos ou parênteses. O caractere pode aparecer em comentário de código, não em copy.
- **Proibido adjetivo de prova social:** "aclamado", "obra-prima", "sucesso", "best-seller", "mais vendido", "premiado". O catálogo tem 5 avaliações no total. Nada disso é verificável.
- **Proibido selo de estrelas ou contagem de avaliações** em qualquer ficha desta versão.
- **Proibido número de popularidade** ("obra nº 1", "Pop Rank"). O campo do catálogo é ordem de listagem herdada, não venda.
- **Nenhum detalhe de enredo pode ser inventado.** Toda frase sobre uma obra sai de `.claude/catalogo.json`, de `Relatórios/ficha-kdp-a-saga-italiana-17-08-2026.md` ou da PDP publicada em `/o-mestre-das-tormentas`. Se a informação não estiver numa dessas três fontes, ela não entra.
- **Um único formulário na página**, no herói. Dois formulários criariam IDs HTML duplicados (`EMAIL`, `JOB_TITLE`, `OPT_IN`), o que quebra acessibilidade e confunde a Brevo. A seção de fechamento tem botão que rola de volta para ele.
- **Peso alvo:** HTML na faixa de `/arquetipos` (52 KB). A home tem 138 KB e é o contra-exemplo.
- **Sem vídeo, sem iframe, sem script de terceiro** além do `gtag` e do `analytics.js` que já são padrão do site.
- **Links da Amazon:** sempre URL longa `https://www.amazon.com.br/dp/<ASIN>?tag=falcojc-20&ascsubtag=romance-historico-<slug>`. Nunca link curto: o `analytics.js` extrai o ASIN do padrão `/dp/XXXXXXXXXX` e link curto chega ao GA4 como `(sem asin)`.
- **ASINs, conferidos em 24/08:** O Siciliano `B0D9WS272F` · O Mestre das Tormentas `B08XYL4QZY` · Amor e Ódio `B0D8RTCPNP` · A Saga Italiana `B0HFPS4K6R`.
- **Não existe test runner neste repositório.** O ciclo de verificação de cada tarefa é: build do Eleventy → checagem do HTML gerado por `grep` → medição no navegador. Onde este plano diz "teste", é isso.
- **Branch:** `feature/lp-romance-historico`, que já existe e já contém o spec. Não commitar na `main`.

---

## Estrutura de arquivos

| Arquivo | Responsabilidade | Ação |
|---|---|---|
| `romance-historico/index.html` | A página inteira: markup, CSS inline, JSON-LD, script de reveal | Criar |
| `eleventy.config.js` | Registrar a pasta nova no passthrough, senão ela não chega ao `_site` | Modificar |
| `sitemap.xml.njk` | Entrada da URL nova, para o Search Console achar | Modificar |
| `_includes/` (rodapé) | Link para a página nova, já que o menu principal está cheio | Modificar |
| `.claude/bienal/gera_qr.py` | Gerar o PNG do QR com UTM | Criar |

**Por que um arquivo só para a página:** é o padrão vivo do repositório (`/arquetipos`, `/audiolivro`, `/o-mestre-das-tormentas` são todos assim), o Eleventy os trata como passthrough puro, e quebrar isso agora criaria um segundo padrão de LP sem ganho.

---

### Task 1: Esqueleto, registro no build e head

**Files:**
- Create: `romance-historico/index.html`
- Modify: `eleventy.config.js` (bloco de `addPassthroughCopy`, perto da linha 10)
- Modify: `sitemap.xml.njk` (depois da entrada de `/arquetipos/`)

**Interfaces:**
- Produces: a rota `/romance-historico/` servida pelo `_site`, e o arquivo onde todas as tarefas seguintes escrevem.

- [ ] **Step 1: Criar a página com head completo e body vazio**

Criar `romance-historico/index.html`. O bloco de `@font-face` e o `:root` devem ser copiados **literalmente** de `arquetipos/index.html` (linhas 37 a 55), para não divergir o design system.

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-R2ZQZ51DEK"></script>
<script src="/analytics.js" defer></script>
<title>Romance histórico: por onde começar · Domenico Falco</title>
<meta name="description" content="Não sabe qual romance histórico ler primeiro? Três portas de entrada no catálogo de Domenico Falco, e o que separa romance histórico de romance de época.">
<link rel="canonical" href="https://www.livrosdofalco.com.br/romance-historico/">
<meta name="robots" content="index,follow">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="preload" as="font" type="font/woff2" href="/fonts/eb-garamond-143e88.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="/fonts/cinzel-63551c.woff2" crossorigin>
<style>
  /* COLAR AQUI as linhas 37 a 55 de arquetipos/index.html: os sete @font-face
     e o bloco :root com --bg, --bg-alt, --card, --card-border, --gold,
     --gold-bright, --red, --text, --text-muted, --cost */
  *{box-sizing:border-box;margin:0;padding:0;}
  html{scroll-behavior:smooth;}
  body{background:var(--bg);color:var(--text);font-family:'EB Garamond',serif;font-size:19px;line-height:1.65;}
  h1,h2,h3,.display{font-family:'Cinzel',serif;letter-spacing:.03em;}
  a{color:inherit;text-decoration:none;}
  img{display:block;max-width:100%;height:auto;}
  .wrap{max-width:1180px;margin:0 auto;padding:0 28px;}
  .eyebrow{font-family:'Cinzel',serif;font-size:13px;letter-spacing:.28em;text-transform:uppercase;color:var(--gold);}
  :focus-visible{outline:2px solid var(--gold-bright);outline-offset:3px;}
  .skip{position:absolute;left:-9999px;}
  .skip:focus{left:16px;top:12px;z-index:99;background:var(--gold);color:#0b0908;padding:10px 16px;border-radius:2px;}
</style>
<script>document.documentElement.classList.add('js');</script>
</head>
<body>
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
<main id="conteudo">
</main>
</body>
</html>
```

Atenção ao `height:auto` na regra de `img`: sem ele, o atributo HTML `height` vira o valor usado e qualquer `aspect-ratio` é ignorado. Esse bug já custou uma rodada de correção na `/arquetipos`.

- [ ] **Step 2: Registrar a pasta no Eleventy**

Em `eleventy.config.js`, logo depois da linha `eleventyConfig.addPassthroughCopy("arquetipos");`:

```js
  eleventyConfig.addPassthroughCopy("romance-historico");
```

- [ ] **Step 3: Adicionar ao sitemap**

Em `sitemap.xml.njk`, depois do bloco `<url>` de `/arquetipos/`:

```xml
  <url>
    <loc>https://www.livrosdofalco.com.br/romance-historico/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
```

- [ ] **Step 4: Buildar e verificar que a rota existe**

```bash
npx.cmd @11ty/eleventy && ls _site/romance-historico/index.html && grep -c "romance-historico" _site/sitemap.xml
```

Esperado: o `ls` lista o arquivo, e o `grep -c` devolve `1`. Se o `ls` falhar, o passthrough do Step 2 não foi salvo.

- [ ] **Step 5: Verificar o title no HTML gerado**

```bash
grep -o "<title>[^<]*</title>" _site/romance-historico/index.html
```

Esperado: `<title>Romance histórico: por onde começar · Domenico Falco</title>`

- [ ] **Step 6: Commit**

```bash
git add romance-historico/index.html eleventy.config.js sitemap.xml.njk
git commit -m "LP /romance-historico: esqueleto, head e registro no build"
```

---

### Task 2: Seção 1, herói e formulário de captura

**Files:**
- Modify: `romance-historico/index.html` (dentro de `<main id="conteudo">`, e regras novas no `<style>`)

**Interfaces:**
- Consumes: as variáveis CSS do `:root` da Task 1.
- Produces: `#lp-form` (o único formulário da página) e a âncora `#comecar`, usados pela Task 6.

- [ ] **Step 1: Escrever o markup do herói**

Dentro de `<main id="conteudo">`:

```html
<section class="hero">
  <div class="wrap hero-inner">
    <div class="hero-copy">
      <p class="eyebrow">Romance histórico brasileiro · 30 obras de Domenico Falco</p>
      <h1>Até onde você iria pela sua <em>família</em>?<br>E o que essa escolha lhe custaria?</h1>
      <p class="lead">Romance histórico de alta imersão, em que o passado não é cenário decorativo: é o que força pessoas comuns a decisões impossíveis. Guerra, exílio, fome, ocupação. Ninguém sai ileso.</p>
      <p class="lead-sub">Não sabe por onde começar? <a href="#portas">Veja as três portas de entrada</a>.</p>
    </div>
    <div class="hero-form" id="comecar">
      <p class="form-title">Ouça um romance completo, de graça</p>
      <p class="form-sub">O audiolivro de <strong>O Comandante</strong>, 1h51 de narração em 23 faixas MP3 para baixar e ouvir offline: no carro, na cozinha, na caminhada. Sem tela, sem anúncio e sem depender de sinal.</p>
      <!-- FORMULÁRIO: colar aqui o bloco do Step 2 -->
    </div>
  </div>
</section>
```

O `<em>família</em>` existe para o CSS poder dourar só essa palavra, mesmo padrão do H1 da `/arquetipos`.

- [ ] **Step 2: Colar o formulário da Brevo**

Copiar o `<form>` de `audiolivro/index.html` **sem alterar o `action`, os `name` dos campos nem o campo-armadilha**. O campo do nome se chama `JOB_TITLE` por uma limitação da conta da Brevo, e renomear quebra o cadastro. O `input[name=email_address_check]` é o honeypot antibot da própria Brevo e precisa continuar escondido e presente, porque o captcha está desligado nesta família de páginas.

Três mudanças permitidas, e só elas:
1. O texto do `<button>` passa a ser `Receber o audiolivro grátis`.
2. Adicionar, antes do `</form>`, o campo de origem:
   ```html
   <input type="hidden" name="ORIGEM" value="romance-historico">
   ```
3. O `placeholder` do nome continua `Como quer ser chamada`.

- [ ] **Step 3: Escrever o CSS do herói**

Acrescentar ao `<style>`:

```css
  /* HERO */
  .hero{padding:64px 0 56px;border-bottom:1px solid var(--card-border);}
  .hero-inner{display:grid;grid-template-columns:1.15fr .85fr;gap:56px;align-items:start;}
  .hero h1{font-size:clamp(30px,4.4vw,52px);line-height:1.15;margin:14px 0 22px;}
  .hero h1 em{font-style:normal;color:var(--gold);}
  .lead{font-size:20px;color:var(--text);max-width:34em;}
  .lead-sub{margin-top:14px;font-size:17px;color:var(--text-muted);}
  .lead-sub a{color:var(--gold-bright);border-bottom:1px solid rgba(201,161,58,.4);}
  .hero-form{background:var(--card);border:1px solid var(--card-border);border-radius:3px;padding:28px 26px;}
  .form-title{font-family:'Cinzel',serif;font-size:21px;color:var(--gold-bright);margin-bottom:10px;}
  .form-sub{font-size:16px;color:var(--text-muted);margin-bottom:20px;}
  .campo{margin-bottom:14px;}
  .campo label{display:block;font-size:14px;color:var(--text-muted);margin-bottom:6px;}
  .input{width:100%;padding:12px 14px;background:var(--bg);border:1px solid var(--card-border);border-radius:2px;color:var(--text);font-family:inherit;font-size:17px;}
  .optin{display:flex;gap:10px;align-items:flex-start;font-size:15px;color:var(--text-muted);margin:16px 0 18px;cursor:pointer;}
  .optin input{margin-top:5px;flex-shrink:0;}
  .btn{display:inline-block;font-family:'Cinzel',serif;font-size:16px;letter-spacing:.08em;padding:14px 26px;border-radius:2px;border:1px solid var(--gold);color:var(--gold-bright);background:transparent;cursor:pointer;transition:background .2s,color .2s;}
  .btn:hover{background:var(--gold);color:#0b0908;}
  .btn.solid{background:var(--gold);color:#0b0908;font-weight:600;}
  .btn.solid:hover{background:var(--gold-bright);}
  .btn.full{width:100%;}
  .lp-privacy{font-size:13px;color:var(--text-muted);margin-top:14px;line-height:1.45;}
  .input--hidden{display:none;}
  @media (max-width:900px){
    .hero{padding:40px 0 36px;}
    .hero-inner{grid-template-columns:1fr;gap:34px;}
  }
```

O `grid-template-columns:1fr` no mobile põe o formulário logo abaixo do H1, o que é o comportamento desejado: a ação principal continua acima da dobra no celular, que é onde está o público da Bienal.

- [ ] **Step 4: Buildar e conferir que há exatamente um formulário**

```bash
npx.cmd @11ty/eleventy && grep -c "<form" _site/romance-historico/index.html && grep -c "ORIGEM" _site/romance-historico/index.html
```

Esperado: `1` e `1`. Se o primeiro der `2`, há formulário duplicado, o que este plano proíbe.

- [ ] **Step 5: Conferir no navegador que o formulário aparece acima da dobra no mobile**

Abrir o preview (`preview_start` com a config `livrosdofalco`), redimensionar para o preset `mobile` (375x812), navegar até `/romance-historico/` e rodar:

```js
document.querySelector('#lp-form').getBoundingClientRect().top
```

Esperado: valor abaixo de 900. Se for maior, o herói está comprido demais e o lead nunca vê o formulário sem rolar duas telas.

- [ ] **Step 6: Commit**

```bash
git add romance-historico/index.html
git commit -m "LP /romance-historico: heroi e formulario de captura"
```

---

### Task 3: Seção 2, as três portas de entrada

**Files:**
- Modify: `romance-historico/index.html`

**Interfaces:**
- Consumes: `.btn` e as variáveis de cor da Task 2.
- Produces: a âncora `#portas` (referenciada no herói) e a classe `.book-card`, que o `analytics.js` usa para disparar `click_to_amazon`.

**Sobre as imagens destas fichas, decidido em 24/08:** cada porta leva uma **cena**, não a
capa do livro. A tese da página é "não pode ser catálogo", e capa de livro é a linguagem de
catálogo; cena é linguagem editorial. A capa continua aparecendo na seção do omnibus e na
própria PDP da Amazon, então o produto não fica sem rosto.

As três cenas **já estão geradas** em `romance-historico/media/`, convertidas por
`.claude/perf/gera_cenas_romance_historico.py` a partir das artes originais em
`2. Produto/StoryTelling/Romance Histórico`. Os originais são PNG e JPG de 2816x1536 pesando
de 3 a 9 MB; a saída é WebP de 800px:

| Cena | Origem | Peso final |
|---|---|---|
| `o-siciliano-cafezal.webp` | Imagem 2 (O Trabalho e a Terra Cafezal) | 78 KB |
| `mestre-das-tormentas-naufragio.webp` | Cap 9.3 O Silêncio do Mar | 44 KB |
| `amor-e-odio-clandestino.webp` | O Romance Clandestino (Paco e Carmen) | 32 KB |

154 KB no total, contra 20,8 MB de origem. **Não usar os originais em hipótese alguma**, e não
regerar com largura maior que 800px: a ficha renderiza a 367px numa grade de 3 colunas, e 800
já é o dobro, o suficiente para tela retina.

O `vercel.json` ganhou a regra de cache de um ano para `/romance-historico/media/`, no mesmo
padrão de `/o-mestre-das-tormentas/media/`.

**Contexto que o implementador precisa:** a classe `book-card` não é decorativa. O `analytics.js` (linha 36) faz `link.closest('.book-card')` para descobrir de qual obra veio o clique. Sem essa classe no elemento que envolve o link, o evento vai para o GA4 sem identificar a obra. E como o `h3` de cada ficha é o nome do livro, o relatório passa a mostrar qual porta converte.

- [ ] **Step 1: Escrever o markup das três portas**

Os textos abaixo já foram conferidos contra as fontes autorizadas. **Não reescrever, não "melhorar", não adicionar detalhe de enredo.**

```html
<section class="portas" id="portas">
  <div class="wrap">
    <p class="eyebrow">Três portas, não trinta</p>
    <h2>Por onde começar</h2>
    <p class="sec-lead">Trinta títulos paralisam. Escolha o chão histórico que te interessa e comece por ele: cada um destes três abre um caminho diferente dentro do mesmo catálogo.</p>

    <div class="grid-portas">

      <article class="book-card porta">
        <img class="cena" src="/romance-historico/media/o-siciliano-cafezal.webp" alt="Colheita de café numa fazenda brasileira do início do século XX" width="800" height="436" loading="lazy" decoding="async">
        <p class="ambient">Sicília e Brasil, 1880 a 1943</p>
        <p class="perfil">O épico de família</p>
        <h3>O Siciliano</h3>
        <p class="gancho">Uma disputa de terras custa o pai de Matteo. Ele cruza o Atlântico e recomeça do zero nas fazendas de café de Vassouras, no Rio de Janeiro, antes de a família se mudar para São Paulo. Décadas depois, volta à Sicília para acertar o que deixou por resolver.</p>
        <a class="btn" href="https://www.amazon.com.br/dp/B0D9WS272F?tag=falcojc-20&amp;ascsubtag=romance-historico-o-siciliano" target="_blank" rel="noopener">Ler O Siciliano</a>
      </article>

      <article class="book-card porta">
        <img class="cena" src="/romance-historico/media/mestre-das-tormentas-naufragio.webp" alt="Navio naufragando em tempestade, com um bote salva-vidas ao lado" width="800" height="446" loading="lazy" decoding="async">
        <p class="ambient">Sete mares, a partir de 1700</p>
        <p class="perfil">A aventura do desconhecido</p>
        <h3>O Mestre das Tormentas</h3>
        <p class="gancho">Filho de uma cozinheira, criado nos becos de Londres. Dado como morto num naufrágio no Pacífico Sul, John Storm ressurge nas águas asiáticas e atravessa a Rota da Seda atrás do único caminho de volta que ainda importa: para casa, e para quem ele deixou para trás.</p>
        <a class="btn" href="https://www.amazon.com.br/dp/B08XYL4QZY?tag=falcojc-20&amp;ascsubtag=romance-historico-mestre-das-tormentas" target="_blank" rel="noopener">Ler O Mestre das Tormentas</a>
      </article>

      <article class="book-card porta">
        <img class="cena" src="/romance-historico/media/amor-e-odio-clandestino.webp" alt="Casal abraçado sob a chuva, ele em uniforme militar, sob um arco de pedra" width="800" height="436" loading="lazy" decoding="async">
        <p class="ambient">Andaluzia, anos 1930</p>
        <p class="perfil">O amor em tempo de guerra</p>
        <h3>Amor e Ódio</h3>
        <p class="gancho">Uma paixão proibida em famílias que a Guerra Civil Espanhola vai dilacerar. Enquanto um ditador sobe ao poder, cada escolha custa alguém, e ninguém escolhe sem pagar.</p>
        <a class="btn" href="https://www.amazon.com.br/dp/B0D8RTCPNP?tag=falcojc-20&amp;ascsubtag=romance-historico-amor-e-odio" target="_blank" rel="noopener">Ler Amor e Ódio</a>
      </article>

    </div>
  </div>
</section>
```

A sobrelinha de ambientação (`.ambient`) vem **antes** do rótulo de perfil de propósito: é o que o olho reconhece primeiro e o que o buscador indexa como cenário histórico.

- [ ] **Step 2: Escrever o CSS das portas**

```css
  /* PORTAS */
  .portas{padding:64px 0;background:var(--bg-alt);}
  .portas h2{font-size:clamp(26px,3.2vw,38px);margin:12px 0 16px;}
  .sec-lead{font-size:18px;color:var(--text-muted);max-width:52em;margin-bottom:38px;}
  .grid-portas{display:grid;grid-template-columns:repeat(3,1fr);gap:26px;}
  .porta{background:var(--card);border:1px solid var(--card-border);border-radius:3px;padding:28px 24px;display:flex;flex-direction:column;}
  .capa{width:132px;height:auto;border:1px solid var(--card-border);border-radius:2px;margin-bottom:20px;}
  /* Cena: largura total do card, sangrando ate a borda interna do padding */
  .cena{width:calc(100% + 48px);margin:-28px -24px 20px;height:auto;border-radius:3px 3px 0 0;}
  .ambient{font-family:'Cinzel',serif;font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:10px;}
  .perfil{font-size:15px;color:var(--cost);font-style:italic;margin-bottom:4px;}
  .porta h3{font-size:24px;margin-bottom:14px;}
  .gancho{font-size:17px;color:var(--text-muted);margin-bottom:24px;flex-grow:1;}
  .porta .btn{align-self:flex-start;}
  @media (max-width:900px){
    .portas{padding:44px 0;}
    .grid-portas{grid-template-columns:1fr;gap:18px;}
  }
```

O `flex-grow:1` no `.gancho` faz os três botões alinharem na mesma altura mesmo com ganchos de tamanhos diferentes, sem precisar cortar texto.

- [ ] **Step 3: Buildar e conferir os três ASINs e as três classes**

```bash
npx.cmd @11ty/eleventy && grep -c "book-card" _site/romance-historico/index.html && grep -o "dp/B0[A-Z0-9]\{8\}" _site/romance-historico/index.html | sort -u
```

Esperado: `3`, e exatamente estes três ASINs: `B0D8RTCPNP`, `B08XYL4QZY`, `B0D9WS272F`.

- [ ] **Step 4: Conferir que nenhum termo proibido entrou**

```bash
grep -i -E "aclamad|obra-prima|best.?seller|mais vendido|premiad|★|estrelas|popularidade" _site/romance-historico/index.html; echo "exit: $?"
```

Esperado: nenhuma linha, e `exit: 1`. Qualquer resultado aqui é violação das Global Constraints.

- [ ] **Step 5: Commit**

```bash
git add romance-historico/index.html
git commit -m "LP /romance-historico: as tres portas de entrada"
```

---

### Task 4: Seção 3, A Saga Italiana e os dois estados de promoção

**Files:**
- Modify: `romance-historico/index.html`

**Interfaces:**
- Consumes: `.book-card`, `.btn` das tarefas anteriores.
- Produces: a classe `.promo-on`, que liga o estado de promoção, e o elemento `.selo-promo`.

**Contexto:** esta seção tem dois estados e eles alternam quatro vezes em dez dias (A Saga Italiana grátis de 31/08 a 04/09, O Siciliano grátis de 05 a 09/09). Ligar e desligar precisa ser **troca de uma classe no `<body>`**, não reescrita de markup, porque quem vai operar isso é o Julio, no meio de uma feira, do celular se preciso.

- [ ] **Step 1: Escrever o markup da seção**

```html
<section class="omnibus">
  <div class="wrap">
    <p class="eyebrow">O passo seguinte</p>
    <h2>A Saga Italiana</h2>
    <p class="sec-lead">Se O Siciliano te pegou, ele é um terço de uma história maior. A edição especial reúne três romances completos, de três famílias que não se cruzam, cobrindo quase um século da imigração italiana para as Américas.</p>

    <div class="book-card omni-card">
      <img class="capa capa-omni" src="/covers/a-saga-italiana.webp" alt="Capa de A Saga Italiana, edição especial da trilogia" width="400" height="598" loading="lazy" decoding="async">
      <ul class="omni-livros">
        <li><strong>Os Dois Irmãos</strong> <span>Campânia a Mendoza, a partir de 1860</span></li>
        <li><strong>O Siciliano</strong> <span>Sicília e Brasil, 1880 a 1943</span></li>
        <li><strong>Os Italianos</strong> <span>Calábria, Nova York e São Paulo, 1892 ao século XXI</span></li>
      </ul>
      <p class="omni-extra">A edição traz conteúdo que não está nos volumes avulsos: prefácio do autor, uma linha do tempo que encaixa as três histórias no mesmo século e uma comparação entre as três famílias.</p>

      <p class="preco"><span class="de">R$ 29,70 comprados avulsos</span> <strong class="por">R$ 19,90 na edição especial</strong></p>
      <p class="selo-promo">Grátis na Amazon até <span data-promo-fim>04 de setembro</span></p>

      <a class="btn solid" href="https://www.amazon.com.br/dp/B0HFPS4K6R?tag=falcojc-20&amp;ascsubtag=romance-historico-saga-italiana" target="_blank" rel="noopener">
        <span class="cta-normal">Quero a Edição Especial</span>
        <span class="cta-promo">Baixar grátis e, se gostar, avaliar</span>
      </a>
    </div>
  </div>
</section>
```

- [ ] **Step 2: Escrever o CSS, incluindo a alternância de estado**

```css
  /* OMNIBUS */
  .omnibus{padding:64px 0;}
  .omnibus h2{font-size:clamp(26px,3.2vw,38px);margin:12px 0 16px;}
  .omni-card{background:var(--card);border:1px solid var(--card-border);border-radius:3px;padding:32px 28px;max-width:760px;}
  .capa-omni{width:168px;}
  .omni-livros{list-style:none;margin-bottom:22px;}
  .omni-livros li{padding:10px 0;border-bottom:1px solid var(--card-border);}
  .omni-livros li:last-child{border-bottom:0;}
  .omni-livros strong{font-family:'Cinzel',serif;font-size:18px;color:var(--gold-bright);}
  .omni-livros span{display:block;font-size:15px;color:var(--text-muted);margin-top:2px;}
  .omni-extra{font-size:16px;color:var(--text-muted);margin-bottom:24px;}
  .preco{font-size:18px;margin-bottom:22px;}
  .preco .de{color:var(--text-muted);text-decoration:line-through;margin-right:10px;}
  .preco .por{color:var(--gold-bright);font-size:22px;}

  /* Estado de promocao: desligado por padrao, ligado por .promo-on no body */
  .selo-promo{display:none;}
  .cta-promo{display:none;}
  body.promo-on .selo-promo{display:inline-block;background:var(--gold);color:#0b0908;font-family:'Cinzel',serif;font-size:14px;letter-spacing:.08em;padding:8px 14px;border-radius:2px;margin-bottom:20px;}
  body.promo-on .preco{display:none;}
  body.promo-on .cta-normal{display:none;}
  body.promo-on .cta-promo{display:inline;}
```

- [ ] **Step 3: Documentar a operação no próprio arquivo**

Logo antes de `</body>`, deixar o comentário que explica como ligar. Ele existe porque quem vai operar não é quem escreveu:

```html
<!-- PROMOCAO GRATIS: para ligar, trocar <body> por <body class="promo-on"> e
     ajustar a data dentro de [data-promo-fim] e o ASIN do CTA se o titulo em
     promocao nao for a Saga Italiana.
     Calendario acordado em 24/08:
       31/08 a 04/09  A Saga Italiana (B0HFPS4K6R), fim "04 de setembro"
       05/09 a 09/09  O Siciliano     (B0D9WS272F), fim "09 de setembro"
     Fora dessas janelas o body fica sem a classe. -->
```

- [ ] **Step 4: Verificar que o estado normal esconde o selo**

```bash
npx.cmd @11ty/eleventy
```

No navegador, em `/romance-historico/`:

```js
getComputedStyle(document.querySelector('.selo-promo')).display
```

Esperado: `"none"`.

- [ ] **Step 5: Verificar que o estado de promoção funciona**

No mesmo navegador:

```js
document.body.classList.add('promo-on');
[getComputedStyle(document.querySelector('.selo-promo')).display,
 getComputedStyle(document.querySelector('.preco')).display,
 getComputedStyle(document.querySelector('.cta-promo')).display]
```

Esperado: `["inline-block", "none", "inline"]`. Ou seja, o selo aparece, o preço some e o CTA troca de texto. Depois rodar `document.body.classList.remove('promo-on')` para não confundir a inspeção seguinte.

- [ ] **Step 6: Commit**

```bash
git add romance-historico/index.html
git commit -m "LP /romance-historico: secao da Saga Italiana com os dois estados de promocao"
```

---

### Task 5: Seção 4, definição do gênero, e o JSON-LD

**Files:**
- Modify: `romance-historico/index.html`

**Interfaces:**
- Produces: o bloco `<script type="application/ld+json">` com `FAQPage` e `ItemList`.

**Contexto:** esta seção vem **depois** das portas de propósito. Para o tráfego pago, que fica 4 segundos na página, um bloco conceitual antes das obras é obstáculo. Para a IA, que lê a página inteira, a posição é indiferente. É o bloco que ChatGPT e Perplexity citam, e por isso ele precisa de par pergunta/resposta explícito, tanto no texto visível quanto no JSON-LD.

- [ ] **Step 1: Escrever o markup da seção**

```html
<section class="genero">
  <div class="wrap">
    <p class="eyebrow">Antes de escolher</p>
    <h2>O que é romance histórico, e o que não é</h2>

    <div class="grid-genero">
      <div class="col-genero">
        <h3>Romance de época</h3>
        <p>Usa o passado como cenário decorativo e idealizado. Bailes, rituais de corte, salões, uma trama romântica leve por cima. O período é moldura: troque o século e a história continua de pé.</p>
      </div>
      <div class="col-genero destaque">
        <h3>Romance histórico</h3>
        <p>Usa o passado como pressão. O período é justamente o que força a escolha: guerra, fome, exílio, ocupação, perseguição. Troque o século e a história desaparece, porque ela só existe por causa daquilo.</p>
      </div>
    </div>

    <p class="fecho">Não escrevemos sobre bailes de porcelana. Escrevemos sobre o preço que se paga para manter os seus vivos.</p>
  </div>
</section>
```

- [ ] **Step 2: Escrever o CSS**

```css
  /* GENERO */
  .genero{padding:64px 0;background:var(--bg-alt);border-top:1px solid var(--card-border);}
  .genero h2{font-size:clamp(26px,3.2vw,38px);margin:12px 0 32px;}
  .grid-genero{display:grid;grid-template-columns:1fr 1fr;gap:26px;margin-bottom:34px;}
  .col-genero{background:var(--card);border:1px solid var(--card-border);border-radius:3px;padding:26px 24px;}
  .col-genero.destaque{border-color:var(--gold);}
  .col-genero h3{font-size:21px;margin-bottom:12px;color:var(--text-muted);}
  .col-genero.destaque h3{color:var(--gold-bright);}
  .col-genero p{font-size:17px;color:var(--text-muted);}
  .fecho{font-family:'Cinzel',serif;font-size:clamp(19px,2.4vw,26px);line-height:1.4;color:var(--gold-bright);max-width:24em;}
  @media (max-width:900px){
    .genero{padding:44px 0;}
    .grid-genero{grid-template-columns:1fr;gap:16px;}
  }
```

- [ ] **Step 3: Adicionar o JSON-LD**

Colar dentro do `<head>`, logo antes de `</head>`:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "O que é romance histórico?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Romance histórico é a ficção em que o período histórico funciona como pressão sobre os personagens, e não como cenário. Guerra, fome, exílio, ocupação e perseguição são o que força as escolhas da trama: retirado o contexto histórico, a história deixa de existir."
          }
        },
        {
          "@type": "Question",
          "name": "Qual a diferença entre romance histórico e romance de época?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "O romance de época usa o passado como cenário decorativo e idealizado, com foco em bailes, rituais de corte e tramas românticas leves; o período é moldura e pode ser trocado sem que a história mude. O romance histórico usa o passado como causa: o período é o que produz o conflito e determina o custo das decisões dos personagens."
          }
        },
        {
          "@type": "Question",
          "name": "Por qual romance histórico de Domenico Falco começar?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Depende do cenário histórico de interesse. Para imigração italiana e drama de família, O Siciliano, ambientado entre a Sicília e as fazendas de café do Brasil de 1880 a 1943. Para aventura marítima, O Mestre das Tormentas, sobre John Storm, dos becos de Londres à Rota da Seda a partir de 1700. Para guerra e paixão proibida, Amor e Ódio, ambientado na Andaluzia dos anos 1930 durante a Guerra Civil Espanhola."
          }
        }
      ]
    },
    {
      "@type": "ItemList",
      "name": "Romances históricos de Domenico Falco: por onde começar",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "item": {
            "@type": "Book",
            "name": "O Siciliano",
            "author": {"@type": "Person", "name": "Domenico Falco"},
            "inLanguage": "pt-BR",
            "genre": "Romance histórico",
            "identifier": {"@type": "PropertyValue", "propertyID": "ASIN", "value": "B0D9WS272F"},
            "url": "https://www.amazon.com.br/dp/B0D9WS272F"
          }
        },
        {
          "@type": "ListItem",
          "position": 2,
          "item": {
            "@type": "Book",
            "name": "O Mestre das Tormentas",
            "author": {"@type": "Person", "name": "Domenico Falco"},
            "inLanguage": "pt-BR",
            "genre": "Romance histórico",
            "identifier": {"@type": "PropertyValue", "propertyID": "ASIN", "value": "B08XYL4QZY"},
            "url": "https://www.amazon.com.br/dp/B08XYL4QZY"
          }
        },
        {
          "@type": "ListItem",
          "position": 3,
          "item": {
            "@type": "Book",
            "name": "Amor e Ódio",
            "author": {"@type": "Person", "name": "Domenico Falco"},
            "inLanguage": "pt-BR",
            "genre": "Romance histórico",
            "identifier": {"@type": "PropertyValue", "propertyID": "ASIN", "value": "B0D8RTCPNP"},
            "url": "https://www.amazon.com.br/dp/B0D8RTCPNP"
          }
        }
      ]
    }
  ]
}
</script>
```

As URLs dentro do JSON-LD vão **sem** a tag de afiliado. Dado estruturado é declaração sobre a obra, não link de venda, e sujar com parâmetro de campanha só atrapalha o casamento da entidade.

- [ ] **Step 4: Validar que o JSON-LD é JSON válido**

```bash
npx.cmd @11ty/eleventy && python -c "import re,json,io; h=io.open('_site/romance-historico/index.html',encoding='utf-8').read(); b=re.findall(r'<script type=\"application/ld\+json\">(.*?)</script>', h, re.S); [json.loads(x) for x in b]; print('blocos JSON-LD validos:', len(b))"
```

Esperado: `blocos JSON-LD validos: 1`. Se estourar exceção, há vírgula sobrando ou aspas não escapadas.

- [ ] **Step 5: Commit**

```bash
git add romance-historico/index.html
git commit -m "LP /romance-historico: definicao do genero e JSON-LD de FAQ e ItemList"
```

---

### Task 6: Fechamento, rodapé, reveal e navegação

**Files:**
- Modify: `romance-historico/index.html`
- Modify: o rodapé compartilhado. Localizar com `grep -rl "Como Associado da Amazon" --include="*.html" . | grep -v _site | grep -v node_modules`

**Contexto:** o menu principal do site não aguenta mais item (8px de folga em 1280px), então a ligação com o resto do site é só pelo rodapé e pelo sitemap. Mesma decisão da `/arquetipos`.

- [ ] **Step 1: Escrever a seção de fechamento**

Ela não repete o formulário: rola de volta para o único que existe.

```html
<section class="fecho-cta">
  <div class="wrap">
    <!-- CENA DO AUDIOLIVRO: ver nota abaixo. Enquanto o arquivo nao existir,
         deixar a secao sem imagem. Nunca cair no original de 2816px. -->
    <h2>Comece ouvindo, sem pagar nada</h2>
    <p class="sec-lead">O audiolivro de O Comandante inteiro, 1h51 em 23 faixas para baixar. Se a história te pegar, os outros trinta títulos estão a um clique.</p>
    <a class="btn solid" href="#comecar">Receber o audiolivro grátis</a>
  </div>
</section>
```

**Cena do audiolivro, pendência com dono definido.** O Julio vai colocar em
`2. Produto/StoryTelling/Romance Histórico` as artes do podcast de O Comandante, do romance de
Dante com Helga. Em 24/08 elas ainda não tinham chegado ao disco. Quando chegarem:

1. Acrescentar a entrada ao dicionário `CENAS` em
   `.claude/perf/gera_cenas_romance_historico.py`, com o slug `o-comandante-dante-helga`.
2. Rodar o script. Ele é idempotente e não toca nos originais.
3. Inserir a imagem no lugar do comentário acima:

```html
    <img class="cena cena-solta" src="/romance-historico/media/o-comandante-dante-helga.webp" alt="Dante e Helga, personagens do romance O Comandante" width="800" height="436" loading="lazy" decoding="async">
```

**Ela vai aqui, no fechamento, e nunca no herói.** O elemento LCP desta página é texto, que
chega junto com o HTML. Pôr uma cena acima da dobra transfere o LCP para uma imagem e reabre a
armadilha do preload que já custou uma rodada de correção na home em 24/08.

CSS da variante solta (sem sangria, porque não está dentro de um card):

```css
  .cena-solta{width:min(100%,620px);margin:0 auto 26px;border-radius:3px;}
```

- [ ] **Step 2: CSS do fechamento**

```css
  .fecho-cta{padding:64px 0 72px;text-align:center;border-top:1px solid var(--card-border);}
  .fecho-cta h2{font-size:clamp(24px,3vw,34px);margin-bottom:14px;}
  .fecho-cta .sec-lead{margin:0 auto 28px;}
```

- [ ] **Step 3: Copiar o rodapé da /arquetipos**

Copiar o bloco `<footer>` inteiro de `arquetipos/index.html` (a partir da linha 705) para dentro desta página, antes de `</body>`. Ele já contém a divulgação obrigatória do Amazon Associates ("Como Associado da Amazon, eu ganho com compras qualificadas"), que **é exigência contratual em qualquer página com link de afiliado**. Sem ela, a penalidade prevista é encerramento da conta.

Copiar junto o CSS do rodapé de `arquetipos/index.html`.

- [ ] **Step 4: Adicionar o link no rodapé de todo o site**

No arquivo de rodapé compartilhado localizado acima, adicionar, na mesma lista onde já aparece o link de `/arquetipos/`:

```html
<a href="/romance-historico/">Romance histórico</a>
```

- [ ] **Step 5: Adicionar o reveal com rede de segurança**

Antes de `</body>`:

```html
<script>
(function(){
  var alvos = document.querySelectorAll('.porta, .omni-card, .col-genero');
  function mostrarTudo(){ alvos.forEach(function(el){ el.classList.add('is-visible'); }); }
  if (!('IntersectionObserver' in window)) { mostrarTudo(); return; }
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(e){ if (e.isIntersecting) { e.target.classList.add('is-visible'); io.unobserve(e.target); } });
  }, {rootMargin: '0px 0px -10% 0px'});
  alvos.forEach(function(el){ io.observe(el); });
  // Rede de seguranca: aba em segundo plano nao compoe frames, entao o
  // IntersectionObserver pode nunca disparar e a pagina abriria vazia.
  setTimeout(mostrarTudo, 2000);
})();
</script>
```

E o CSS correspondente, que só esconde quando o JS está vivo:

```css
  .js .porta,.js .omni-card,.js .col-genero{opacity:0;transform:translateY(14px);transition:opacity .5s ease,transform .5s ease;}
  .js .porta.is-visible,.js .omni-card.is-visible,.js .col-genero.is-visible{opacity:1;transform:none;}
  @media (prefers-reduced-motion:reduce){
    .js .porta,.js .omni-card,.js .col-genero{opacity:1;transform:none;transition:none;}
  }
```

O `.js` no seletor vem da linha `document.documentElement.classList.add('js')` que está no `<head>` desde a Task 1: sem JavaScript, o conteúdo nunca fica invisível.

- [ ] **Step 6: Verificar que o conteúdo aparece mesmo sem o observer**

No navegador, em `/romance-historico/`:

```js
Array.from(document.querySelectorAll('.porta')).map(e => getComputedStyle(e).opacity)
```

Esperado: `["1","1","1"]` depois de a página estar visível por 2 segundos.

- [ ] **Step 7: Verificar a divulgação do Associates**

```bash
npx.cmd @11ty/eleventy && grep -c "Como Associado da Amazon" _site/romance-historico/index.html
```

Esperado: `1`. Zero aqui é violação de contrato com a Amazon, não detalhe estético.

- [ ] **Step 8: Commit**

```bash
git add romance-historico/index.html
git commit -m "LP /romance-historico: fechamento, rodape, reveal e link no rodape do site"
```

---

### Task 7: Verificação final, peso e acessibilidade

**Files:** nenhum arquivo novo. Esta tarefa é o portão de qualidade antes do merge.

- [ ] **Step 1: Medir o peso do HTML**

```bash
npx.cmd @11ty/eleventy && ls -la _site/romance-historico/index.html _site/arquetipos/index.html _site/index.html
```

Esperado: a página nova na faixa de `arquetipos` (~52 KB) ou menor. Se passar de 70 KB, revisar o que entrou de CSS a mais.

- [ ] **Step 2: Conferir que as quatro capas carregam e não causam layout shift**

```js
Array.from(document.querySelectorAll('.capa')).map(i => i.naturalWidth + 'x' + i.naturalHeight + ' → ' + Math.round(i.getBoundingClientRect().width) + 'px')
```

Esperado: quatro entradas, todas com `naturalWidth` maior que zero. `0x0` significa caminho de imagem errado. E conferir que a altura renderizada não é igual ao atributo `height` do HTML: se `o-siciliano` renderizar 436px de altura em vez de ~199, o `height:auto` do CSS não está sendo aplicado, que é o bug exato que a `/arquetipos` já teve.

- [ ] **Step 3: Conferir hierarquia de headings**

```js
Array.from(document.querySelectorAll('h1,h2,h3')).map(e => e.tagName + ': ' + e.textContent.trim().slice(0,42))
```

Esperado: exatamente **um** `h1`, seguido de `h2` por seção e `h3` dentro delas. Mais de um `h1` derruba a nota de acessibilidade e confunde o Google Ads na leitura de relevância.

- [ ] **Step 4: Conferir contraste e ausência de erro no console**

```js
[...document.querySelectorAll('a,button')].filter(e => !e.textContent.trim() && !e.getAttribute('aria-label')).length
```

Esperado: `0`. E o console do navegador precisa estar sem erro. O site inteiro está em 100 de acessibilidade desde 22/08, e esta página não pode ser a que derruba.

- [ ] **Step 5: Testar o formulário de verdade**

Preencher o formulário no preview com um e-mail real de teste e enviar. Confirmar que redireciona para `/audiolivro/obrigado` e que o cadastro aparece na Brevo com `ORIGEM = romance-historico`.

**Gotcha conhecido:** o `generate_lead` da página de obrigado tem trava de contagem dupla em `localStorage`. Se o e-mail de teste já tiver vindo pela `/audiolivro` antes, a conversão pode não ser contada de novo. Testar com um e-mail que nunca passou pelo funil, senão o resultado é ambíguo.

- [ ] **Step 6: Rodar a página no preset mobile**

Redimensionar para `mobile` (375x812), recarregar e conferir que nada estoura na horizontal:

```js
document.documentElement.scrollWidth <= window.innerWidth
```

Esperado: `true`. `false` significa overflow horizontal, que no celular é o defeito mais visível que existe.

- [ ] **Step 7: Commit final e preparar o merge**

```bash
git add -A
git commit -m "LP /romance-historico: verificacao final de peso, acessibilidade e mobile"
git log --oneline main..HEAD
```

**Não fazer merge na `main` sem aprovação do Julio.** O protocolo do projeto é: branch, preview local, aprovação, merge. Entregar o link `http://localhost:8080/romance-historico/` junto com o pedido de aprovação.

---

### Task 8: QR code da Bienal

**Files:**
- Create: `.claude/bienal/gera_qr.py`
- Create: `.claude/bienal/qr-bienal-romance-historico.png` (gerado)

**Contexto:** o Julio vai à Bienal em 07/09 sem stand, circulando. Ele guarda uma arte com o QR na galeria de fotos do celular, porque a rede do Anhembi em dia de feira é ruim. O QR aponta para a LP, não para a Amazon: apontando para a loja, o evento não deixa e-mail nem medição própria.

- [ ] **Step 1: Escrever o gerador**

```python
# -*- coding: utf-8 -*-
"""Gera o QR code da Bienal 2026 apontando para a LP /romance-historico."""
import qrcode

URL = ("https://www.livrosdofalco.com.br/romance-historico/"
       "?utm_source=bienal&utm_medium=qrcode&utm_campaign=bienal2026")

qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # 30% de tolerancia:
    box_size=20,                                        # foto amassada, tela
    border=4,                                           # riscada, luz ruim
)
qr.add_data(URL)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save("qr-bienal-romance-historico.png")
print("gerado:", img.size, "px ·", URL)
```

O `ERROR_CORRECT_H` não é exagero: o QR vai ser lido de uma foto na tela de um celular, por outro celular, com reflexo e em movimento.

- [ ] **Step 2: Gerar**

```bash
cd .claude/bienal && python -m pip install qrcode[pil] --quiet && python gera_qr.py
```

Esperado: `gerado: (perto de 1000, perto de 1000) px` e o PNG na pasta.

- [ ] **Step 3: Conferir que o QR resolve para a URL certa**

Ler o PNG com o celular ou com `python -c "from pyzbar.pyzbar import decode; from PIL import Image; print(decode(Image.open('qr-bienal-romance-historico.png'))[0].data.decode())"`.

Esperado: a URL completa com os três parâmetros UTM. Um QR com UTM errado é pior que QR nenhum, porque a medição da feira vira lixo silencioso.

- [ ] **Step 4: Commit**

```bash
git add .claude/bienal/
git commit -m "QR code da Bienal 2026 apontando para a LP com UTM"
```

**Fica com o Julio, fora deste plano:** a arte que envolve o QR (imagem para a galeria de fotos) e o texto impresso. O texto precisa dizer que O Siciliano está grátis, porque de 05 a 09/09 ele está, e esse é o "desconto da Bienal" real. Promocode do tipo "Bienal10off" não existe: o KDP não oferece cupom para autor de eBook, e a Oferta Relâmpago não roda na `amazon.com.br`.
