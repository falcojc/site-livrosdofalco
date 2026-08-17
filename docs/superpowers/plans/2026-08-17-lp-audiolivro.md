# LP /audiolivro · Plano de implementação

> **Para quem executa:** use `superpowers:subagent-driven-development` (recomendado) ou
> `superpowers:executing-plans` para tocar tarefa a tarefa. Os passos usam `- [ ]` para
> marcação.

**Objetivo:** publicar uma página de captura em `/audiolivro` que entrega o audiolivro de
O Comandante em MP3 offline em troca do e-mail, e uma página de obrigado que entrega os
arquivos na hora e só então oferece a compra na Amazon.

**Arquitetura:** duas páginas HTML estáticas, no mesmo padrão de `/newsletter` que já roda
em produção. O formulário posta direto para a Brevo, que redireciona para a página de
obrigado. Nenhum banco, nenhum backend, nenhum JavaScript próprio no caminho do envio. Os
arquivos de áudio são reencodados para 64kbps mono e servidos pelo CDN da Vercel.

**Stack:** HTML e CSS puros, Eleventy 3 só como copiador (passthrough), ffmpeg para o
áudio, Python 3.13 para o script de lote, Brevo para lista e formulário, GA4 para medição.

**Spec de origem:** `docs/superpowers/specs/2026-08-17-lp-audiolivro-design.md`

**Diretório de trabalho:** a Task 1 roda a partir da **raiz do projeto** (a pasta que contém
`Site/` e `2. Produto/`), porque toca no material de origem do audiolivro. As Tasks 2 a 5
rodam de dentro de `Site/livrosdofalco`, que é o repositório do site.

## Restrições globais

- **Toda página nova referencia `/analytics.js`.** Nunca copiar o snippet do gtag solto.
  Já houve gap histórico em que Blog e `/newsletter` ficaram sem tag nenhuma por isso.
- **Toda pasta nova de página precisa entrar no passthrough** do `eleventy.config.js`, ou
  não é copiada para `_site` e não vai ao ar.
- **Nada de travessão (—) em texto visível.** Usar vírgula, dois-pontos ou parênteses.
- **Tokens visuais do site:** dourado `--gold`, fundo escuro, tipografia serifada. Copiar do
  shell de `newsletter/index.html`, não inventar paleta nova.
- **Links da Amazon sempre no padrão aberto** `https://link.amazon/XXXXX`. O listener de
  `click_to_amazon` casa por hostname e esse domínio já é reconhecido.
- **Nunca push direto na `main`.** Trabalho todo na branch `feature/lp-audiolivro`, que já
  existe e já contém o spec.
- **Nenhuma prova social por avaliação** em qualquer texto. São 5 avaliações e a média real
  é 3,4 estrelas.
- **O arquivo de origem do áudio nunca é alterado.** O script lê de `2. Produto/...` e
  escreve dentro do repo do site.

## Estrutura de arquivos

| Arquivo | Responsabilidade |
|---|---|
| `.claude/audiolivro/prepara_audio.py` | Converte os 22 capítulos para 64kbps mono, aplica tags e capa, gera o pacote. Ferramenta, fica fora das pastas de material do Falco |
| `audio/o-comandante/NN-slug.mp3` | Os 22 capítulos servidos |
| `audio/o-comandante/o-comandante-audiolivro.zip` | Pacote "baixar tudo" |
| `audiolivro/index.html` | Página de captura. Um objetivo, zero links de saída |
| `audiolivro/obrigado/index.html` | Entrega dos arquivos, aviso de confirmação, CTA Amazon |
| `eleventy.config.js` | Ganha uma linha de passthrough para `audiolivro` |

---

## Task 1: Preparar os arquivos de áudio

**Arquivos:**
- Criar: `.claude/audiolivro/prepara_audio.py` (na raiz do projeto, não no repo do site)
- Criar: `audio/o-comandante/*.mp3` e o `.zip` (saída do script, dentro do repo do site)

**Interfaces:**
- Produz: 22 arquivos nomeados `NN-slug.mp3` (`01-lembrancas.mp3` … `22-epilogo.mp3`) e
  `o-comandante-audiolivro.zip`. As tarefas 3 e 5 dependem exatamente desses nomes.

- [ ] **Passo 1: Escrever o script de conversão**

Criar `C:\Users\falco\OneDrive\BackUp\2. Carreira\1. JF Design\Projetos\Livros Dô\.claude\audiolivro\prepara_audio.py`:

```python
"""
Converte os 22 capitulos do audiolivro de O Comandante para o formato de entrega da LP.

Origem: 192kbps estereo, 159MB no total. Voz narrada nao precisa disso.
Saida:  64kbps mono (padrao de audiolivro), ~53MB, com tags ID3 e capa embutida.

Nao hardcodar caminho: o Falco reorganiza a arvore de pastas. Tudo e derivado
subindo ate achar a raiz do projeto, comparando pelo NOME do diretorio (a raiz de
tudo contem "BackUp", entao filtrar pelo caminho inteiro descartaria o projeto).

Uso: python prepara_audio.py
"""

import re
import subprocess
import unicodedata
import zipfile
from pathlib import Path

BITRATE = "64k"
ALBUM = "O Comandante"
ARTISTA = "Domenico Falco"


def raiz_do_projeto():
    for pasta in Path(__file__).resolve().parents:
        if (pasta / "Site").is_dir() and (pasta / "2. Produto").is_dir():
            return pasta
    raise SystemExit("nao achei a raiz do projeto subindo a partir do script")


def slug(texto):
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", sem_acento.lower()).strip("-")


def main():
    raiz = raiz_do_projeto()
    origem = raiz / "2. Produto/Catalogo/Obras Literárias/30. O Comandante/4. Audiobook/Capitulos"
    site = raiz / "Site/livrosdofalco"
    destino = site / "audio/o-comandante"
    capa = site / "covers/o-comandante.jpg"
    destino.mkdir(parents=True, exist_ok=True)

    # "Capítulo 7 - A Oportunidade.mp3" -> (7, "A Oportunidade")
    padrao = re.compile(r"Cap[íi]tulo\s+(\d+)\s*-\s*(.+)", re.IGNORECASE)
    faixas = []
    for arq in origem.glob("*.mp3"):
        m = padrao.match(arq.stem)
        if m:
            faixas.append((int(m.group(1)), m.group(2).strip(), arq))
    faixas.sort()

    if len(faixas) != 22:
        raise SystemExit(f"esperava 22 capitulos, achei {len(faixas)}")

    gerados = []
    for numero, titulo, arq in faixas:
        saida = destino / f"{numero:02d}-{slug(titulo)}.mp3"
        cmd = [
            "ffmpeg", "-y", "-i", str(arq), "-i", str(capa),
            "-map", "0:a", "-map", "1:v", "-c:v", "copy",
            "-disposition:v", "attached_pic",
            "-ac", "1", "-b:a", BITRATE,
            "-map_metadata", "-1",
            "-metadata", f"title={numero}. {titulo}",
            "-metadata", f"artist={ARTISTA}",
            "-metadata", f"album={ALBUM}",
            "-metadata", f"track={numero}/22",
            "-id3v2_version", "3",
            str(saida),
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        gerados.append(saida)
        print(f"  {saida.name}  {saida.stat().st_size / 1e6:.1f} MB")

    pacote = destino / "o-comandante-audiolivro.zip"
    with zipfile.ZipFile(pacote, "w", zipfile.ZIP_STORED) as z:
        for arq in gerados:
            z.write(arq, arq.name)

    total = sum(a.stat().st_size for a in gerados) / 1e6
    print(f"\n{len(gerados)} capitulos, {total:.1f} MB")
    print(f"pacote: {pacote.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
```

- [ ] **Passo 2: Rodar o script**

```bash
python ".claude/audiolivro/prepara_audio.py"
```

Esperado: 22 linhas de arquivo, cada uma entre 1,5 e 3,5 MB, e um total impresso entre
45 e 60 MB. Se der `esperava 22 capitulos, achei N`, parar: o padrão de nome mudou na pasta
de origem e o regex precisa ser revisto antes de seguir.

- [ ] **Passo 3: Verificar o formato de saída**

```bash
ffprobe -v error -show_entries stream=channels,bit_rate -show_entries format=duration -of default=noprint_wrappers=1 "Site/livrosdofalco/audio/o-comandante/01-lembrancas.mp3"
```

Esperado: `channels=1`, `bit_rate` perto de 64000. Se vier `channels=2`, o `-ac 1` não foi
aplicado e os arquivos estão com o dobro do tamanho necessário.

- [ ] **Passo 4: Verificar que a soma respeita o critério de aceite**

```bash
du -ch "Site/livrosdofalco/audio/o-comandante"/*.mp3 | tail -1
```

Esperado: total abaixo de 60MB. Este é o critério 6 do spec.

- [ ] **Passo 5: Conferir a capa e o título numa faixa**

```bash
ffprobe -v error -show_entries format_tags=title,artist,album,track -of default=noprint_wrappers=1 "Site/livrosdofalco/audio/o-comandante/05-helga.mp3"
```

Esperado: `title=5. Helga`, `artist=Domenico Falco`, `album=O Comandante`, `track=5/22`.

- [ ] **Passo 6: Commit**

```bash
cd "Site/livrosdofalco" && git add audio/o-comandante && git commit -m "Audiolivro de O Comandante em 64kbps mono para a LP"
```

---

## Task 2: Página de captura

**Arquivos:**
- Criar: `audiolivro/index.html`
- Modificar: `eleventy.config.js` (uma linha de passthrough)

**Interfaces:**
- Consome: nada da Task 1 (a página de captura não lista arquivos).
- Produz: o formulário com `action` provisória, que a Task 4 substitui pela URL real da
  Brevo, e o `id="lp-form"` que a Task 4 usa para localizar o formulário.

- [ ] **Passo 1: Registrar a pasta no passthrough**

Em `eleventy.config.js`, logo depois da linha do `newsletter`:

```js
  eleventyConfig.addPassthroughCopy("newsletter");
  eleventyConfig.addPassthroughCopy("audiolivro");
```

Sem isso o Eleventy ignora a pasta e a página não existe no site publicado.

- [ ] **Passo 2: Criar a página**

Criar `audiolivro/index.html`. Copiar o shell de `newsletter/index.html` (bloco `<head>`,
variáveis de cor, tipografia e o CSS do formulário da Brevo, incluindo o `<svg>` de loading
dentro do botão de envio, que o script da Brevo espera encontrar e sem o qual a barra
quebra em silêncio). Trocar o miolo por:

```html
<main class="lp">
  <section class="lp-hero">
    <p class="eyebrow">Audiolivro completo, de graça</p>
    <h1>O audiolivro de O Comandante, completo, no seu celular</h1>
    <p class="lp-sub">
      1h55 de narração em 22 capítulos, para baixar e ouvir offline: no carro, na cozinha,
      na caminhada. Sem anúncio e sem precisar olhar para a tela.
    </p>

    <div class="lp-form-wrap">
      <!-- FORM DA BREVO: shell copiado de newsletter/index.html.
           action provisoria, substituida na Task 4. -->
      <form id="lp-form" method="POST" action="BREVO_ACTION_URL_PENDENTE" data-type="subscription">
        <input class="input" type="text" id="EMAIL" name="EMAIL" placeholder="Seu melhor e-mail" required />
        <input class="input" type="text" id="JOB_TITLE" name="JOB_TITLE" maxlength="200" placeholder="Seu nome" required />
        <label class="lp-optin">
          <input type="checkbox" value="1" id="OPT_IN" name="OPT_IN" required />
          <span>Quero receber o audiolivro e as novidades do autor por e-mail.</span>
        </label>
        <button type="submit" class="btn solid">Quero ouvir</button>
        <input type="text" name="email_address_check" value="" class="input--hidden" style="display:none">
        <input type="hidden" name="locale" value="pt">
        <p class="lp-privacy">Seu e-mail não é compartilhado com ninguém. Você sai da lista quando quiser, em um clique.</p>
      </form>
    </div>
  </section>

  <section class="lp-sample">
    <h2>Ouça um trecho antes de decidir</h2>
    <audio controls preload="none" src="/audio/o-comandante-amostra.mp3" data-obra="O Comandante"></audio>
  </section>

  <section class="lp-oque">
    <h2>O que você recebe</h2>
    <ul>
      <li><strong>22 capítulos</strong> em arquivos separados, cerca de 2,4MB cada</li>
      <li><strong>1h55 de narração</strong>, do começo ao fim, sem corte</li>
      <li><strong>Toca em qualquer lugar:</strong> celular, computador ou som do carro</li>
      <li><strong>Funciona offline</strong>, depois de baixar não precisa de internet</li>
    </ul>
  </section>

  <section class="lp-autor">
    <img src="/author-domenico-falco.jpg" alt="Domenico Falco, autor de O Comandante" width="96" height="96">
    <p><strong>Domenico Falco</strong> tem 30 romances publicados, quase todos sobre pessoas
    comuns atravessando guerras, travessias e recomeços.</p>
  </section>
</main>
```

Regras da página, que são o motivo dela existir: **nenhum `<a>` que saia da página**, nem no
cabeçalho nem no rodapé. O topo leva só o logo, sem link. O rodapé leva uma linha de texto,
sem menu.

- [ ] **Passo 3: Confirmar que a tag de analytics está na página**

```bash
grep -c "analytics.js" audiolivro/index.html
```

Esperado: `1`. Se vier `0`, a página nasce sem medição nenhuma, que é o gap histórico do
projeto.

- [ ] **Passo 4: Confirmar que não há link de saída**

```bash
grep -nE '<a [^>]*href="(https?:|/)' audiolivro/index.html
```

Esperado: nenhuma linha. Qualquer resultado aqui é uma fuga de tráfego numa página que tem
um objetivo só.

- [ ] **Passo 5: Build e verificação no localhost**

```bash
npx @11ty/eleventy --serve
```

Abrir `http://localhost:8080/audiolivro/`. Conferir: o formulário aparece sem rolar a
página no celular (largura 375px), a amostra toca, e não existe menu.

- [ ] **Passo 6: Commit**

```bash
git add audiolivro/index.html eleventy.config.js && git commit -m "Pagina de captura /audiolivro"
```

---

## Task 3: Página de obrigado

**Arquivos:**
- Criar: `audiolivro/obrigado/index.html`

**Interfaces:**
- Consome: os nomes de arquivo gerados na Task 1 (`audio/o-comandante/NN-slug.mp3` e o zip).
- Produz: o evento `generate_lead` com `event_label: 'audiolivro'`.

- [ ] **Passo 1: Criar a página**

Mesmo shell visual da Task 2. Miolo:

```html
<main class="lp">
  <section class="lp-hero">
    <h1>Pronto. Seu audiolivro está aqui embaixo.</h1>
    <p class="lp-sub">Baixe agora, não precisa esperar e-mail nenhum para isso.</p>
    <a class="btn solid" href="/audio/o-comandante/o-comandante-audiolivro.zip" download>
      Baixar o audiolivro completo (22 capítulos)
    </a>
  </section>

  <section class="lp-aviso">
    <p><strong>Confirme seu e-mail.</strong> Acabamos de enviar uma mensagem pedindo
    confirmação. Sem ela você não recebe as novidades do autor, mas o download acima já
    está liberado.</p>
  </section>

  <section class="lp-capitulos">
    <h2>Ou ouça capítulo por capítulo</h2>
    <ol class="cap-list">
      <!-- os 22 <li> entram aqui, gerados pelo comando do Passo 2 -->
    </ol>
  </section>

  <section class="lp-amazon">
    <h2>Prefere ler?</h2>
    <p>O Comandante está na Amazon, em Kindle e Kindle Unlimited.</p>
    <a class="btn" href="https://link.amazon/B02BbXrEH" target="_blank" rel="noopener">
      Ver O Comandante na Amazon
    </a>
  </section>
</main>
```

A ordem importa e não deve ser alterada: entrega, aviso de confirmação, capítulos, e só
então a Amazon. O botão da Amazon é o último elemento da página de propósito.

- [ ] **Passo 2: Gerar os 22 itens da lista a partir dos arquivos reais**

Digitar 22 blocos à mão convida a erro de digitação num link que, se quebrar, quebra
justamente a entrega. Gerar a partir do que existe no disco e das tags que a Task 1 gravou:

```bash
python - <<'PY'
import subprocess, html
from pathlib import Path

pasta = Path("audio/o-comandante")
linhas = []
for arq in sorted(pasta.glob("[0-9][0-9]-*.mp3")):
    titulo = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format_tags=title",
         "-of", "default=noprint_wrappers=1:nokey=1", str(arq)],
        capture_output=True, text=True, check=True).stdout.strip()
    t = html.escape(titulo)
    src = "/" + arq.as_posix()
    linhas.append(
        f'      <li>\n'
        f'        <span class="cap-nome">{t}</span>\n'
        f'        <audio controls preload="none" src="{src}"></audio>\n'
        f'        <a href="{src}" download aria-label="Baixar {t}">Baixar</a>\n'
        f'      </li>'
    )
print("\n".join(linhas))
PY
```

Esperado: 22 blocos `<li>`, do `1. Lembranças` ao `22. Epílogo`. Colar o resultado dentro
do `<ol class="cap-list">`.

- [ ] **Passo 3: Impedir que a página seja indexada**

No `<head>`, obrigatoriamente:

```html
<meta name="robots" content="noindex, nofollow">
```

**Isto não é detalhe de SEO, é o que protege a isca.** Sem `noindex`, o Google acha a
página de obrigado, ela passa a aparecer na busca por "audiolivro O Comandante", e qualquer
pessoa baixa os 22 capítulos sem nunca deixar e-mail. A LP inteira perderia a função.

- [ ] **Passo 4: Disparar o evento de conversão**

No fim do `<body>`:

```html
<script>
  window.addEventListener('load', function () {
    if (typeof gtag === 'function') {
      gtag('event', 'generate_lead', {
        event_category: 'captura',
        event_label: 'audiolivro'
      });
    }
  });
</script>
```

`generate_lead` é reaproveitado de propósito: já está ligado à conversão do Google Ads pela
regra `ads_conversion_Enviar_formul_rio_de_le_1` do GA4. Um evento novo exigiria criar meta
no painel do Ads e esperar validação.

- [ ] **Passo 5: Conferir que todos os 22 arquivos referenciados existem**

```bash
grep -oE '/audio/o-comandante/[0-9]{2}-[a-z0-9-]+\.mp3' audiolivro/obrigado/index.html | sort -u | sed 's|^/||' | while read f; do [ -f "$f" ] || echo "FALTA: $f"; done
```

Esperado: nenhuma saída. Qualquer `FALTA:` é um link quebrado na página de entrega, que é o
pior lugar possível para um 404.

- [ ] **Passo 6: Conferir o noindex**

```bash
grep -c "noindex" audiolivro/obrigado/index.html
```

Esperado: `1`.

- [ ] **Passo 7: Commit**

```bash
git add audiolivro/obrigado/index.html && git commit -m "Pagina de obrigado com entrega e CTA da Amazon"
```

---

## Task 4: Ligar o formulário da Brevo

**Bloqueada** até o Julio criar a lista e o formulário no painel e informar a action URL
(passo a passo na seção 9 do spec). Nada aqui é executável antes disso.

**Arquivos:**
- Modificar: `audiolivro/index.html` (o atributo `action` do `<form id="lp-form">`)

- [ ] **Passo 1: Substituir a action provisória**

Trocar `BREVO_ACTION_URL_PENDENTE` pela URL real, no formato
`https://<id>.sibforms.com/serve/<hash>`.

- [ ] **Passo 2: Confirmar que não sobrou placeholder**

```bash
grep -c "BREVO_ACTION_URL_PENDENTE" audiolivro/index.html
```

Esperado: `0`.

- [ ] **Passo 3: Enviar um cadastro real de teste**

No localhost, preencher com um e-mail de teste do próprio Julio e enviar.

Esperado: o navegador chega em `/audiolivro/obrigado/` e o contato aparece na lista
`Leitores — Audiolivro` no painel da Brevo, com o nome no campo `JOB_TITLE`.

Se o navegador ficar na mesma página mostrando a mensagem de sucesso da Brevo em vez de
redirecionar, o redirecionamento não foi configurado no painel. Corrigir no painel, não no
código: interceptar o submit no JavaScript é o plano B do spec e adiciona uma peça que pode
quebrar em silêncio.

- [ ] **Passo 4: Commit**

```bash
git add audiolivro/index.html && git commit -m "Liga o formulario da LP na lista propria da Brevo"
```

---

## Task 5: Verificação ponta a ponta e publicação

**Arquivos:**
- Modificar: `sitemap.xml.njk` (incluir `/audiolivro/`, nunca a página de obrigado)

- [ ] **Passo 1: Incluir só a página de captura no sitemap**

Adicionar a URL `/audiolivro/` junto das URLs escritas à mão. **Não incluir
`/audiolivro/obrigado/`**, que é `noindex` e não deve ser anunciada ao Google.

- [ ] **Passo 2: Confirmar o evento no GA4**

Com o DebugView do GA4 aberto, percorrer o fluxo no localhost: abrir `/audiolivro/`, tocar
a amostra, enviar o formulário, chegar na página de obrigado e clicar no botão da Amazon.

Esperado, nesta ordem: `page_view`, `play_audiobook_sample`, `page_view`, `generate_lead`
(rótulo `audiolivro`), `click_to_amazon`.

- [ ] **Passo 3: Medir a performance da página de captura**

```bash
npx lighthouse http://localhost:8080/audiolivro/ --only-categories=performance --preset=desktop --quiet --chrome-flags="--headless"
```

Esperado: performance acima de 90. É a página que recebe tráfego pago, e o público chega
com 4 segundos de paciência.

- [ ] **Passo 4: Pedir aprovação do Julio no localhost**

Mandar o link `http://localhost:8080/audiolivro/` junto da pergunta. Regra do projeto:
toda pergunta sobre subir para produção vai com o link do localhost junto.

Pedir junto a única verificação que não dá para automatizar e que é critério de aceite do
spec: **baixar o pacote num celular real e conferir** que os 22 capítulos aparecem na ordem
certa, com o nome do capítulo e a capa do livro no player.

- [ ] **Passo 5: Conferir que nada ficou fora do commit**

```bash
git status --short
```

Esperado: nenhuma saída. Existe histórico de capas modificadas ficarem fora de cinco
commits seguidos numa sessão com commits picados.

- [ ] **Passo 6: Merge e publicação**

Só depois da aprovação. Push da branch, PR, merge na `main`. Deploy da Vercel é automático
no push da `main`.

Para confirmar que o deploy chegou de verdade, olhar o `Last-Modified` de um arquivo novo,
por exemplo `/audio/o-comandante/01-lembrancas.mp3`. Não olhar o HTML da home: o CDN serve
cache antigo com `X-Vercel-Cache: HIT` e query string não fura esse cache.

---

## Pendências que não bloqueiam

- **Capítulos 18 e 21 estão os dois nomeados "Silêncio"** nos arquivos de origem. O script
  vai gerar `18-silencio.mp3` e `21-silencio.mp3`, nomes distintos, então nada quebra. Mas a
  lista da página de obrigado vai mostrar dois capítulos com o mesmo nome. Se for engano, o
  ideal é renomear na origem antes da Task 1 e rodar o script de novo.
- **A segunda porta de captura** (no ponto de saída para a Amazon) tem spec próprio a
  escrever, e deve ser testada isolada da LP para não confundir as duas medições.
