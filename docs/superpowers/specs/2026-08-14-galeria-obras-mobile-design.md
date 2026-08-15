# Galeria "Obras" da Home: reordenação, separação Única/Série e correção do scroll no mobile

## Contexto

A seção "Obras" da Home (`index.html`, `.books-grid`) lista as 30 obras num grid `auto-fill` que vira 1 coluna no mobile. Sem nenhuma forma de agrupamento ou truncamento, isso gera ~30 cards empilhados verticalmente (cada um com capa + tags + título + sinopse + botão, ~500-700px de altura), um scroll extremamente longo no celular.

Esta mudança sobe junto com a troca de 6 capas já preparada na branch `feature/capas-bienal-2026` (ver contexto da sessão: pastas de capa da Bienal, KDP já aprovado).

## Objetivo

1. Nova ordem de exibição das 30 obras, definida pelo autor.
2. Separar o conteúdo em duas seções: "Edições Únicas" (26 obras) e "Livros em Série" (4 obras, 2 sagas).
3. Truncar a seção "Edições Únicas" para reduzir o scroll inicial no mobile, com expansão sob demanda.
4. Manter o rastreamento de eventos GA4 consistente com o padrão existente em `analytics.js`.

## Fora de escopo

- Páginas de categoria (`categoria/*/index.html`) não são alteradas — mantêm sua lista própria de obras, sem truncamento nem reordenação.
- Contagem dinâmica no texto do botão ("+20 obras") — o número fica escrito fixo no HTML, igual ao resto do site (sem template engine na Home).
- Cadastro da obra "John Storm" — não existe, era um apelido de "O Mestre das Tormentas" (resolvido na conversa).

## Ordem final das 30 obras

**Seção 1 — Edições Únicas** (26 obras, nesta ordem):
1. O Comandante · 2. O Siciliano · 3. Um Lugar ao Sol · 4. A Vila · 5. Amor e Ódio · 6. Os Dois Irmãos · 7. A Indústria do Vício · 8. O Asilo · 9. O Tesouro Maldito · 10. A Teia · 11. Sangue Frio · 12. Joana · 13. O Reino · 14. A Casa dos Prazeres · 15. O Jesuíta · 16. Os Templários · 17. Julius · 18. Mariana & José Inácio · 19. O Mestre das Tormentas · 20. O Marciano · 21. Akira · 22. Os Italianos · 23. A Viagem · 24. O Que Eu Lembro Deles · 25. Os Refugiados · 26. Reflexões Sobre a Vida

**Seção 2 — Livros em Série** (4 obras, nesta ordem):
1. Destinos Cruzados · 2. Destinos Cruzados: Parte 2 · 3. O Explorador · 4. O Explorador: Em Busca do Desconhecido

O Mestre das Tormentas fica em Únicas (decisão do autor): embora seja uma saga de 3 livros, é vendida como uma edição única (um arquivo, mais páginas), diferente de Destinos Cruzados e O Explorador, que são obras publicadas separadamente na Amazon.

## Estrutura e comportamento

**HTML:**
- Os 30 `<div class="book-card">` existentes são reordenados fisicamente no HTML na ordem acima (mesma marcação, mesmos ids, mesmas imagens — só a posição no documento muda).
- Um `<h3>` ou divisor visual de seção é inserido antes do primeiro card de "Livros em Série", com o rótulo "Livros em Série".
- Os 20 cards de Únicas a partir do 7º (Julius em diante, i.e. todos exceto os 6 primeiros: O Comandante, O Siciliano, Um Lugar ao Sol, A Vila, Amor e Ódio, Os Dois Irmãos) recebem uma classe `book-card--hidden`.
- Um botão `<button id="obras-ver-mais" class="btn small">Ver todas as 26 obras</button>` é inserido ao final da seção Únicas, antes da seção Série.
- "Livros em Série" não é truncada — os 4 cards ficam sempre visíveis, sem collapse.

**CSS:**
- `.book-card--hidden { display: none; }` — some do fluxo (não afeta o grid dos visíveis).
- Quando a classe `.obras-expandido` é aplicada num ancestral (ou removida de cada `.book-card--hidden`), os cards reaparecem no grid.

**JS (script inline na Home, perto do grid — mesmo padrão dos outros scripts inline já existentes em `index.html`):**
- Uma função `expandirObrasUnicas()` remove `book-card--hidden` de todos os cards afetados e esconde o botão `#obras-ver-mais`.
- Clique em `#obras-ver-mais`: chama `expandirObrasUnicas()` e, na sequência, dispara `gtag('event', 'click_ver_mais_obras', { event_category: 'obras', event_label: 'unicas' })` diretamente (gtag já é global via `analytics.js`, carregado antes no `<head>`) — não precisa de um novo bloco no listener delegado de `analytics.js`, porque o clique já é tratado aqui.
- Ao carregar a página, um script no load lê `location.hash`; se o elemento alvo tem a classe `book-card--hidden`, chama `expandirObrasUnicas()` antes do scroll nativo do navegador rolar até a âncora. Isso evita quebrar links diretos existentes (redes sociais, ads) que apontam para uma obra específica do meio da lista. Esse caminho não dispara `click_ver_mais_obras` (não houve clique no botão) — se quiser medir também esse caso no futuro, é um evento separado, fora deste escopo.

## Capas (já prontas, entram no mesmo commit)

As 6 capas atualizadas já estão na branch `feature/capas-bienal-2026` (`covers/um-lugar-ao-sol.jpg`, `destinos-cruzados.jpg`, `reflexoes-sobre-a-vida.jpg`, `o-reino.jpg`, `o-explorador-desconhecido.jpg`, `o-explorador.jpg`), aprovadas no KDP. Sobem juntas com a reestruturação da galeria, num único PR/deploy.

## Testes / verificação manual

- Desktop (≥1280px): grid mostra 6 cards de Únicas + botão + 4 cards de Série sem scroll excessivo; clicar no botão revela os 20 restantes sem quebrar o grid.
- Mobile (375px, preview do Browser pane): confirmar que a altura de scroll inicial da seção Obras cai bem em relação ao estado atual (30 cards abertos).
- Testar link direto com hash para uma obra escondida (ex. `/#o-tesouro-maldito`) e confirmar que expande automaticamente antes de rolar.
- Verificar no `dataLayer` (console) que `click_ver_mais_obras` dispara ao clicar no botão.
- Conferir visualmente as 6 capas novas na seção Únicas e Série.
