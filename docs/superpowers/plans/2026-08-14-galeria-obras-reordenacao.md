# Reordenação da galeria "Obras" + truncar mobile — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reordenar as 30 obras da Home na ordem definida pelo autor, separar "Edições Únicas" de "Livros em Série", truncar Únicas a 6 cards visíveis com expansão sob demanda (reduz o scroll no mobile), e subir junto as 6 capas já prontas na branch `feature/capas-bienal-2026`.

**Architecture:** Site estático HTML puro (sem framework/build na Home — Eleventy só constrói o Blog). Toda a mudança é em `index.html`: reordenação física dos blocos `.book-card` existentes, uma classe CSS (`book-card--hidden`) pra truncar, e um `<script>` inline no fim do documento pra expandir sob clique ou por deep-link de hash. Sem servidor, sem build step, sem test runner no projeto — verificação é manual via preview local (`npm run serve`, já mapeado em `.claude/launch.json` como `blog-eleventy`) e inspeção visual no Browser pane.

**Tech Stack:** HTML/CSS/JS vanilla, gtag (GA4) já carregado globalmente via `analytics.js`.

## Global Constraints

- Branch de trabalho: `feature/capas-bienal-2026` (já existe, já tem as 6 capas prontas e o spec commitado). Não criar branch nova.
- Ordem final das 30 obras é a definida no spec `docs/superpowers/specs/2026-08-14-galeria-obras-mobile-design.md` — copiar exatamente, não improvisar ordem.
- Os primeiros 6 cards de "Edições Únicas" ficam sempre visíveis: O Comandante, O Siciliano, Um Lugar ao Sol, A Vila, Amor e Ódio, Os Dois Irmãos. Os 20 seguintes (Julius em diante, até Reflexões Sobre a Vida) recebem `book-card--hidden`.
- "Livros em Série" (Destinos Cruzados, Destinos Cruzados: Parte 2, O Explorador, O Explorador: Em Busca do Desconhecido) nunca é truncada — sempre visível, sem collapse.
- Nenhum `id`, `href`, `src`, `alt` ou texto de sinopse dos 30 cards muda — só a posição no documento e as duas classes/elementos novos (`book-card--hidden`, botão, divisor de seção).
- Evento GA do botão novo: `gtag('event', 'click_ver_mais_obras', { event_category: 'obras', event_label: 'unicas' })`, disparado só no clique real (não no auto-expand por hash).
- Páginas de `categoria/*/index.html` não são tocadas neste plano.

---

### Task 1: Reordenar os 30 cards, inserir divisor "Livros em Série", corrigir contagem do subtítulo

**Files:**
- Modify: `index.html:1077-1400` (section `#obras` inteira)

**Interfaces:**
- Produces: a `section#obras` com dois blocos `.books-grid` — o primeiro (`id="obras-unicas"`) com os 26 cards de Únicas na nova ordem, o segundo com os 4 cards de Série. Tasks 2-4 dependem do `id="obras-unicas"` existir e dos cards de Série virem depois de um elemento com texto "Livros em Série".

- [ ] **Step 1: Ler o bloco atual completo para confirmar que nada foi editado desde a última leitura**

Ler `index.html` linhas 1077-1400 e conferir que os 30 `id="..."` batem com os já mapeados no spec (nenhuma obra nova, nenhuma removida).

- [ ] **Step 2: Substituir a section inteira pelo bloco reordenado**

Usar Edit em `index.html` com `old_string` = o conteúdo atual completo de `<section id="obras">` até `</section>` (linhas 1077-1400), `new_string` = o bloco abaixo:

```html
<section id="obras">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">Catálogo</div>
      <h2>As Obras</h2>
      <div class="divider"></div>
      <p>Trinta romances, trinta mundos: piratas, samurais, jesuítas, cruzados e sobreviventes atravessando a história.</p>
    </div>

    <div class="books-grid" id="obras-unicas">

      <div class="book-card" id="o-comandante">
        <div class="book-cover"><img src="covers/o-comandante.jpg" alt="O Comandante"></div>
        <div class="book-body">
          <div class="book-tags-row">
            <span class="book-badge">Lançamento</span>
            <div class="book-tag">Entreguerras</div>
          </div>
          <h3>O Comandante</h3>
          <p>Das ruínas da guerra ao topo do império marítimo global, a história de resiliência, perigos no mar e o verdadeiro custo do sucesso de um homem que reconstrói tudo a partir do nada.</p>
          <div class="book-audio">
            <span class="book-audio-label">🎧 Ouça uma amostra do audiobook</span>
            <audio controls preload="none" src="audio/o-comandante-amostra.mp3"></audio>
          </div>
          <a class="btn small" href="https://link.amazon/B02BbXrEH" target="_blank" rel="noopener">Comprar na Amazon</a>
        </div>
      </div>

      <div class="book-card" id="o-siciliano">
        <div class="book-cover"><img src="covers/o-siciliano.jpg" alt="O Siciliano"></div>
        <div class="book-body">
          <div class="book-tag">Imigração Italiana</div>
          <h3>O Siciliano</h3>
          <p>Obrigado a deixar a Sicília após uma disputa de terras, Matteo reconstrói sua vida como imigrante no Rio de Janeiro e em São Paulo, nas primeiras décadas do século XX.</p>
          <a class="btn small" href="https://link.amazon/B08t0ClRq" target="_blank" rel="noopener">Comprar na Amazon</a>
        </div>
      </div>

      <div class="book-card" id="um-lugar-ao-sol">
        <div class="book-cover"><img src="covers/um-lugar-ao-sol.jpg" alt="Um Lugar ao Sol"></div>
        <div class="book-body">
          <div class="book-tag">Nova Iorque, Anos 60/70</div>
          <h3>Um Lugar ao Sol</h3>
          <p>Cinco alunos de um instituto de artes cênicas em Nova Iorque atravessam as grandes transformações culturais das décadas de 1960 e 1970, incluindo a Guerra do Vietnã.</p>
          <a class="btn small" href="https://link.amazon/B0aGQgpeB" target="_blank" rel="noopener">Comprar na Amazon</a>
        </div>
      </div>

      <div class="book-card" id="a-vila">
        <div class="book-cover"><img src="covers/a-vila.jpg" alt="A Vila"></div>
        <div class="book-body">
          <div class="book-tag">Grécia, Século XX</div>
          <h3>A Vila</h3>
          <p>Numa aldeia de pescadores de sardinhas na Grécia do início do século XX, Athena, Andreas e seus quatro filhos vivem um drama familiar de amor, paixão e tragédia.</p>
          <a class="btn small" href="https://link.amazon/B00Abz1w9" target="_blank" rel="noopener">Comprar na Amazon</a>
        </div>
      </div>

      <div class="book-card" id="amor-e-odio">
        <div class="book-cover"><img src="covers/amor-e-odio.jpg" alt="Amor e Ódio"></div>
        <div class="book-body">
          <div class="book-tag">Guerra Civil Espanhola</div>
          <h3>Amor e Ódio</h3>
          <p>Entre a Guerra Civil Espanhola e a Segunda Guerra Mundial, um triângulo amoroso se transforma em traições e crimes passionais e políticos, revelando personalidades tão ambíguas quanto a própria guerra.</p>
          <a class="btn small" href="https://link.amazon/B05nNXv5D" target="_blank" rel="noopener">Comprar na Amazon</a>
        </div>
      </div>

      <div class="book-card" id="os-dois-irmaos">
        <div class="book-cover"><img src="covers/os-dois-irmaos.jpg" alt="Os Dois Irmãos"></div>
        <div class="book-body">
          <div class="book-tag">Itália, 1860</div>
          <h3>Os Dois Irmãos</h3>
          <p>Na Campagna dos anos 1860, dois irmãos italianos atravessam provações que testam os laços de sangue, uma história densa e imprevisível sobre redenção e superação.</p>
          <a class="btn small" href="https://link.amazon/B099y4kAd" target="_blank" rel="noopener">Comprar na Amazon</a>
        </div>
      </div>

      <div class="book-card book-card--hidden" id="a-industria-do-vicio">
        <div class="book-cover"><img src="covers/a-industria-do-vicio.jpg" alt="A Indústria do Vício"></div>
        <div class="book-body">
          <div class="book-tag">Lei Seca</div>
          <h3>A Indústria do Vício</h3>
          <p>Durante a Lei Seca americana, o capo Don Domenico e seu conselheiro Vince constroem um império à sombra da lei nas ruas de Nova Iorque e Atlantic City.</p>
          <a class="btn small" href="https://link.amazon/B09juTmUd" target="_blank" rel="noopener">Comprar na Amazon</a>
        </div>
      </div>

      <div class="book-card book-card--hidden" id="o-asilo">
        <div class="book-cover"><img src="covers/o-asilo.jpg" alt="O Asilo"></div>
        <div class="book-body">
          <div class="book-tag">Drama &amp; Memória</div>
          <h3>O Asilo</h3>
          <p>Em um asilo nos arredores do Rio de Janeiro, em meados do século XX, moradores idosos e enfermos dividem histórias de vida, perda e companheirismo.</p>
          <a class="btn small" href="https://link.amazon/B08KUy5xA" target="_blank" rel="noopener">Comprar na Amazon</a>
        </div>
      </div>

      <div class="book-card book-card--hidden" id="o-tesouro-maldito">
        <div class="book-cover"><img src="covers/o-tesouro-maldito.jpg" alt="O Tesouro Maldito"></div>
        <div class="book-body">
          <div class="book-tag">Piratas &amp; Maldições</div>
          <h3>O Tesouro Maldito</h3>
          <p>No início do século XVI, o capitão Diego García rouba um tesouro asteca e foge amaldiçoado pelos mares do Caribe, enquanto uma criatura misteriosa começa a rondar seu navio.</p>
          <a class="btn small" href="https://link.amazon/B079khqVa" target="_blank" rel="noopener">Comprar na Amazon</a>
        </div>
      </div>

      <div class="book-card book-card--hidden" id="a-teia">
        <div class="book-cover"><img src="covers/a-teia.jpg" alt="A Teia"></div>
        <div class="book-body">
          <div class="book-tag">Drama Urbano</div>
          <h3>A Teia</h3>
          <p>Nascidos na mesma favela carioca, Joca se torna um criminoso poderoso e Helena, promotora pública decidida a desmontar seu império, até seus caminhos se cruzarem de novo.</p>
          <a class="btn small" href="https://link.amazon/B06lJ8s2p" target="_blank" rel="noopener">Comprar na Amazon</a>
        </div>
      </div>

      <div class="book-card book-card--hidden" id="sangue-frio">
        <div class="book-cover"><img src="covers/sangue-frio.jpg" alt="Sangue Frio"></div>
        <div class="book-body">
          <div class="book-tag">Faroeste</div>
          <h3>Sangue Frio</h3>
          <p>O sofrimento e a luta de um homem escravizado desde o nascimento para vencer o preconceito e o ódio impostos à sua condição humana, em meados do século XIX, entre a África e os Estados Unidos.</p>
          <a class="btn small" href="https://link.amazon/B06W7KyzS" target="_blank" rel="noopener">Comprar na Amazon</a>
        </div>
      </div>

      <div class="book-card book-card--hidden" id="joana">
        <div class="book-cover"><img src="covers/joana.jpg" alt="Joana: A Dama da Noite"></div>
        <div class="book-body">
          <div class="book-tag">Belle Époque</div>
          <h3>Joana: A Dama da Noite</h3>
          <p>A história da irreverente Joana, seus familiares, amores e aventuras, durante a primeira metade do século XX, entre a França e o Brasil.</p>
          <a class="btn small" href="https://link.amazon/B08IDAJBy" target="_blank" rel="noopener">Comprar na Amazon</a>
        </div>
      </div>

      <div class="book-card book-card--hidden" id="o-reino">
        <div class="book-cover"><img src="covers/o-reino.jpg" alt="O Reino"></div>
        <div class="book-body">
          <div class="book-tag">Poder &amp; Ambição</div>
          <h3>O Reino</h3>
          <p>Homens poderosos, dispostos a tudo para alcançar o que desejam, inclusive viver para sempre.</p>
          <a class="btn small" href="https://link.amazon/B09rWOUcM" target="_blank" rel="noopener">Comprar na Amazon</a>
        </div>
      </div>

      <div class="book-card book-card--hidden" id="a-casa-dos-prazeres">
        <div class="book-cover"><img src="covers/a-casa-dos-prazeres.jpg" alt="A Casa dos Prazeres"></div>
        <div class="book-body">
          <div class="book-tag">Japão Feudal</div>
          <h3>A Casa dos Prazeres</h3>
          <p>Uma família que, apesar de sofrer uma grande injustiça, consegue se reerguer aproveitando oportunidades inesperadas que a vida lhe oferece, um romance ambientado no Japão feudal.</p>
          <a class="btn small" href="https://link.amazon/B05HgVbe9" target="_blank" rel="noopener">Comprar na Amazon</a>
        </div>
      </div>

      <div class="book-card book-card--hidden" id="o-jesuita">
        <div class="book-cover"><img src="covers/o-jesuita.jpg" alt="O Jesuíta"></div>
        <div class="book-body">
          <div class="book-tag">Fé &amp; Mistério</div>
          <h3>O Jesuíta</h3>
          <p>Sob o capuz de um velho missionário pesa um passado de escolhas difíceis. Entre mapas antigos e ruínas de impérios, uma história sobre fé, culpa e os limites da devoção.</p>
          <a class="btn small" href="https://link.amazon/B0bjfPAhK" target="_blank" rel="noopener">Comprar na Amazon</a>
        </div>
      </div>

      <div class="book-card book-card--hidden" id="os-templarios">
        <div class="book-cover"><img src="covers/os-templarios.jpg" alt="Os Templarios"></div>
        <div class="book-body">
          <div class="book-tag">Cruzadas</div>
          <h3>Os Templarios</h3>
          <p>Dois cavaleiros templários vivem aventuras na Terra Santa e na Europa em busca do Santo Graal.</p>
          <a class="btn small" href="https://link.amazon/B0fxnejMl" target="_blank" rel="noopener">Comprar na Amazon</a>
        </div>
      </div>

      <div class="book-card book-card--hidden" id="julius">
        <div class="book-cover"><img src="covers/julius.jpg" alt="Julius"></div>
        <div class="book-body">
          <div class="book-tag">Roma Antiga</div>
          <h3>Julius</h3>
          <p>Um romano nascido na mesma época de Jesus (Yeshua), que tem sua vida transformada pelo legado do Nazareno.</p>
          <a class="btn small" href="https://link.amazon/B0gm2f63E" target="_blank" rel="noopener">Comprar na Amazon</a>
        </div>
      </div>

      <div class="book-card book-card--hidden" id="mariana-e-jose-inacio">
        <div class="book-cover"><img src="covers/mariana-e-jose-inacio.jpg" alt="Mariana &amp; José Inácio"></div>
        <div class="book-body">
          <div class="book-tag">Grandes Navegações</div>
          <h3>Mariana &amp; José Inácio</h3>
          <p>As aventuras de um casal de portugueses que desembarca no Brasil colonial do século XVI para implantar engenhos e explorar as riquezas geradas pela cana-de-açúcar.</p>
          <a class="btn small" href="https://link.amazon/B0eEyJ9Zy" target="_blank" rel="noopener">Comprar na Amazon</a>
        </div>
      </div>

      <div class="book-card book-card--hidden" id="mestre-das-tormentas">
        <div class="book-cover"><img src="covers/mestre-das-tormentas.jpg" alt="O Mestre das Tormentas"></div>
        <div class="book-body">
          <div class="book-tag">Saga em 3 Livros</div>
          <h3>O Mestre das Tormentas</h3>
          <p>As aventuras de um corsário inglês que se torna pirata durante o século XVIII, percorrendo os principais oceanos da Terra.</p>
          <div style="display:flex;gap:10px;flex-wrap:wrap;">
            <a class="btn small solid" href="/o-mestre-das-tormentas">Conheça a saga</a>
            <a class="btn small" href="https://link.amazon/B01k8LazN" target="_blank" rel="noopener">Comprar na Amazon</a>
          </div>
        </div>
      </div>

      <div class="book-card book-card--hidden" id="o-marciano">
        <div class="book-cover"><img src="covers/o-marciano.jpg" alt="O Marciano"></div>
        <div class="book-body">
          <div class="book-tag">Ficção Científica</div>
          <h3>O Marciano</h3>
          <p>Um raro desvio da ficção histórica de Falco: sob um céu alienígena pairando sobre dunas avermelhadas, um conto especulativo sobre solidão, contato e o desconhecido.</p>
          <a class="btn small" href="https://link.amazon/B01MYHAbP" target="_blank" rel="noopener">Comprar na Amazon</a>
        </div>
      </div>

      <div class="book-card book-card--hidden" id="akira">
        <div class="book-cover"><img src="covers/akira.jpg" alt="Akira: O Senhor das Armas"></div>
        <div class="book-body">
          <div class="book-tag">Japão Imperial</div>
          <h3>Akira: O Senhor das Armas</h3>
          <p>No Japão em plena modernização após o fim do xogunato, o jovem Akira troca a vida simples na fazenda da avó pela disciplina do exército imperial. Ferido e condecorado como herói, reconstrói-se como um dos mais poderosos industriais do ramo de armamentos, "O Senhor das Armas".</p>
          <a class="btn small" href="https://link.amazon/B062ef4xG" target="_blank" rel="noopener">Comprar na Amazon</a>
        </div>
      </div>

      <div class="book-card book-card--hidden" id="os-italianos">
        <div class="book-cover"><img src="covers/os-italianos.jpg" alt="Os Italianos"></div>
        <div class="book-body">
          <div class="book-tag">Entreguerras</div>
          <h3>Os Italianos</h3>
          <p>A história de uma família de italianos em busca de melhores condições de vida na América do Norte e do Sul, uma ficção baseada em fatos reais que atravessa todo o século XX até o início do XXI, retratando os principais eventos históricos do período.</p>
          <a class="btn small" href="https://link.amazon/B0a17JfGu" target="_blank" rel="noopener">Comprar na Amazon</a>
        </div>
      </div>

      <div class="book-card book-card--hidden" id="a-viagem">
        <div class="book-cover"><img src="covers/a-viagem.jpg" alt="A Viagem"></div>
        <div class="book-body">
          <div class="book-tag">Drama no Mediterrâneo</div>
          <h3>A Viagem</h3>
          <p>A bordo do iate de luxo Aurora, três casais jovens e ricos navegam pelo Mediterrâneo, até que o confinamento e o imprevisível coloquem suas crenças e destinos em xeque.</p>
          <a class="btn small" href="https://link.amazon/B0gD3RC5M" target="_blank" rel="noopener">Comprar na Amazon</a>
        </div>
      </div>

      <div class="book-card book-card--hidden" id="o-que-eu-lembro-deles">
        <div class="book-cover"><img src="covers/o-que-eu-lembro-deles.jpg" alt="O Que Eu Lembro Deles"></div>
        <div class="book-body">
          <div class="book-tag">Conflitos na Irlanda do Norte</div>
          <h3>O Que Eu Lembro Deles</h3>
          <p>Kilian e Eileen se apaixonam em Belfast durante os anos mais duros dos conflitos entre católicos e protestantes, um drama sobre amor, tradição e as escolhas que moldam um destino.</p>
          <a class="btn small" href="https://link.amazon/B03B5r7zc" target="_blank" rel="noopener">Comprar na Amazon</a>
        </div>
      </div>

      <div class="book-card book-card--hidden" id="os-refugiados">
        <div class="book-cover"><img src="covers/os-refugiados.jpg" alt="Os Refugiados"></div>
        <div class="book-body">
          <div class="book-tag">Guerra Civil na Síria</div>
          <h3>Os Refugiados</h3>
          <p>Contada pelos próprios personagens, esta é a história de uma família síria de classe média que atravessa a guerra civil e se torna símbolo de resiliência e esperança.</p>
          <a class="btn small" href="https://link.amazon/B0g7NULvj" target="_blank" rel="noopener">Comprar na Amazon</a>
        </div>
      </div>

      <div class="book-card book-card--hidden" id="reflexoes-sobre-a-vida">
        <div class="book-cover"><img src="covers/reflexoes-sobre-a-vida.jpg" alt="Reflexões Sobre a Vida"></div>
        <div class="book-body">
          <div class="book-tag">Ensaio &amp; Reflexão</div>
          <h3>Reflexões Sobre a Vida</h3>
          <p>Reflexões e pensamentos sobre a vida, e também sobre os tempos vividos durante a pandemia.</p>
          <a class="btn small" href="https://link.amazon/B0b0XZSET" target="_blank" rel="noopener">Comprar na Amazon</a>
        </div>
      </div>

    </div>

    <div class="obras-ver-mais-wrap">
      <button type="button" id="obras-ver-mais" class="btn small">Ver todas as 26 obras</button>
    </div>

    <div class="eyebrow obras-subsecao">Livros em Série</div>

    <div class="books-grid">

      <div class="book-card" id="destinos-cruzados">
        <div class="book-cover"><img src="covers/destinos-cruzados.jpg" alt="Destinos Cruzados"></div>
        <div class="book-body">
          <div class="book-tag">Amizade &amp; História</div>
          <h3>Destinos Cruzados</h3>
          <p>Uma inglesa, um chinês e um indiano, três jovens amigos cujas vidas são moldadas pelos grandes acontecimentos históricos das décadas de 1940 e 1950.</p>
          <a class="btn small" href="https://link.amazon/B0hDr3Z3s" target="_blank" rel="noopener">Comprar na Amazon</a>
        </div>
      </div>

      <div class="book-card" id="destinos-cruzados-parte-2">
        <div class="book-cover"><img src="covers/destinos-cruzados-parte-2.jpg" alt="Destinos Cruzados: Parte 2"></div>
        <div class="book-body">
          <div class="book-tag">Espionagem em Hong Kong</div>
          <h3>Destinos Cruzados: Parte 2</h3>
          <p>Já agente do MI6, o jovem William parte para a Hong Kong dos anos 1960 em busca de sua mãe desaparecida, uma missão que mistura espionagem e história pessoal.</p>
          <a class="btn small" href="https://link.amazon/B0admSdvz" target="_blank" rel="noopener">Comprar na Amazon</a>
        </div>
      </div>

      <div class="book-card" id="o-explorador">
        <div class="book-cover"><img src="covers/o-explorador.jpg" alt="O Explorador"></div>
        <div class="book-body">
          <div class="book-tag">Aventura</div>
          <h3>O Explorador</h3>
          <p>A história de um jovem inglês do século XIX, apaixonado por aventuras e ávido por conhecer o mundo.</p>
          <a class="btn small" href="https://link.amazon/B03lGhsxT" target="_blank" rel="noopener">Comprar na Amazon</a>
        </div>
      </div>

      <div class="book-card" id="o-explorador-desconhecido">
        <div class="book-cover"><img src="covers/o-explorador-desconhecido.jpg" alt="O Explorador: Em Busca do Desconhecido"></div>
        <div class="book-body">
          <div class="book-tag">Aventura</div>
          <h3>O Explorador: Em Busca do Desconhecido</h3>
          <p>Resgatado à deriva perto da Antártida e sem memória, o explorador James encontra em Luna, uma cientista argentina, o caminho para novas aventuras em Galápagos e na Amazônia Andina.</p>
          <a class="btn small" href="https://link.amazon/B09nhHaLT" target="_blank" rel="noopener">Comprar na Amazon</a>
        </div>
      </div>

    </div>
  </div>
</section>
```

- [ ] **Step 3: Conferir contagem**

Rodar:
```bash
grep -c 'class="book-card' index.html
grep -c 'book-card--hidden' index.html
```
Expected: primeiro comando retorna `50` (30 cards, mas `book-card--hidden` contém a substring `book-card` também, então cada card escondido casa 2x — ok se o número bater com 30 cards + 20 ocorrências extras de `book-card--hidden`; o teste real é o próximo comando). Segundo comando retorna `20`.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "Reordena galeria Obras e separa Unicas/Serie"
```

---

### Task 2: CSS de truncamento e do botão "Ver mais"

**Files:**
- Modify: `index.html:241-251` (bloco de estilos `.book-cover` até `.book-audio audio`, dentro do `<style>` da seção BOOKS)

**Interfaces:**
- Consumes: classes `book-card--hidden`, `obras-ver-mais-wrap`, `obras-subsecao` criadas na Task 1.
- Produces: `.book-card--hidden{display:none}` — Task 4 (JS) depende de remover exatamente essa classe pra revelar os cards.

- [ ] **Step 1: Adicionar as três regras novas depois de `.book-audio audio`**

Em `index.html`, logo após a linha `.book-audio audio{width:100%;height:34px;}` (dentro do bloco BOOKS), adicionar:

```css
  .book-card--hidden{display:none;}
  .obras-ver-mais-wrap{text-align:center;margin-top:34px;}
  .obras-subsecao{margin-top:56px;}
```

- [ ] **Step 2: Verificar visualmente no preview local**

Rodar o preview (`preview_start` com a config `blog-eleventy` de `.claude/launch.json`, porta 8081) e navegar para `http://localhost:8081/index.html#obras`. Confirmar visualmente: 6 cards de Únicas + botão "Ver todas as 26 obras" + bloco "Livros em Série" com 4 cards, todos visíveis; os 20 cards escondidos não aparecem no grid nem deixam buraco vazio.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "Adiciona CSS de truncamento da galeria Obras"
```

---

### Task 3: JS de expansão, evento GA e deep-link por hash

**Files:**
- Modify: `index.html` — inserir um novo `<script>` logo antes do `</body>` de fechamento (mesma região dos outros `<script>` inline já existentes no arquivo, por volta da linha 1650+; usar Grep por `</body>` para achar a posição exata no momento da implementação, pois a Task 1 desloca todos os números de linha).

**Interfaces:**
- Consumes: `#obras-unicas .book-card--hidden` (Task 1/2), `gtag` (função global já carregada por `analytics.js` antes deste ponto do documento).
- Produces: nenhuma interface consumida por outra task — é o último elo da cadeia.

- [ ] **Step 1: Localizar o ponto de inserção**

```bash
grep -n '</body>' index.html
```
Anotar o número de linha retornado — o novo `<script>` vai imediatamente antes dela.

- [ ] **Step 2: Inserir o script**

Usar Edit com `old_string` = `</body>` (única ocorrência) e `new_string`:

```html
<script>
(function(){
  var btn = document.getElementById('obras-ver-mais');
  function expandirObrasUnicas(){
    document.querySelectorAll('#obras-unicas .book-card--hidden').forEach(function(card){
      card.classList.remove('book-card--hidden');
    });
    var wrap = document.querySelector('.obras-ver-mais-wrap');
    if (wrap) wrap.style.display = 'none';
  }
  if (btn) {
    btn.addEventListener('click', function(){
      expandirObrasUnicas();
      if (typeof gtag === 'function') {
        gtag('event', 'click_ver_mais_obras', { event_category: 'obras', event_label: 'unicas' });
      }
    });
  }
  if (location.hash) {
    var alvo = document.querySelector(location.hash);
    if (alvo && alvo.classList.contains('book-card--hidden')) {
      expandirObrasUnicas();
      alvo.scrollIntoView();
    }
  }
})();
</script>
</body>
```

- [ ] **Step 3: Verificar o clique manualmente no preview**

No Browser pane, com o preview já aberto em `http://localhost:8081/index.html#obras`, usar `read_page` pra achar o `ref` do botão "Ver todas as 26 obras", clicar nele (`computer` `left_click`), depois `read_page` de novo pra confirmar que os 20 cards escondidos agora aparecem e o botão sumiu.

- [ ] **Step 4: Verificar o evento GA no dataLayer**

Com `javascript_tool`, antes do clique, rodar `window.dataLayer = window.dataLayer || []; window.dataLayer.length` pra anotar o tamanho atual. Depois do clique, rodar de novo e confirmar que cresceu, e que `window.dataLayer[window.dataLayer.length-1]` contém `'click_ver_mais_obras'` (o preview local não envia pro GA de verdade — `analytics.js` só chama `gtag('config', ...)` em `livrosdofalco.com.br` — mas o `dataLayer.push` acontece sempre, então dá pra inspecionar aqui).

- [ ] **Step 5: Verificar o deep-link por hash**

Navegar para `http://localhost:8081/index.html#o-tesouro-maldito` (uma obra que está escondida por padrão) e confirmar visualmente que a seção Únicas já abre expandida, com o card de "O Tesouro Maldito" visível.

- [ ] **Step 6: Commit**

```bash
git add index.html
git commit -m "Adiciona expansao da galeria Obras, evento GA e suporte a deep-link"
```

---

### Task 4: Verificação final e handoff pro Falco validar em sandbox

**Files:**
- Nenhum arquivo novo — task de verificação e push.

- [ ] **Step 1: Conferir as 6 capas continuam presentes**

```bash
git status --short
```
Expected: só os commits das Tasks 1-3 aparecem como diferença em relação a `main` (via `git log main..HEAD --oneline`); as 6 capas em `covers/*.jpg` já estavam commitadas antes desta sessão de implementação — confirmar com `git diff main --stat` que elas aparecem na lista de arquivos alterados da branch.

- [ ] **Step 2: Rodar screenshot mobile e desktop do resultado final**

No Browser pane: `resize_window` para `preset: "mobile"`, navegar/recarregar `http://localhost:8081/index.html#obras`, `computer` `screenshot`. Repetir com `preset: "desktop"`. Comparar visualmente contra o estado "antes" (30 cards abertos) já capturado nesta sessão.

- [ ] **Step 3: Push da branch (sem merge — aguardando validação do Falco)**

```bash
git push -u origin feature/capas-bienal-2026
```

- [ ] **Step 4: Reportar o link do preview local pro Falco**

Mensagem final: link `http://localhost:8081` (preview local, branch `feature/capas-bienal-2026`) pra ele validar visualmente antes do merge/deploy. Nenhum merge, push pra `main`, ou deploy Vercel acontece nesta task — fica pra depois da aprovação dele, seguindo o combinado (branch → preview → aprovação → merge é alçada própria só depois do sinal dele).
