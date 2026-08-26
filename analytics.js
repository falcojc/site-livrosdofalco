window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());

// Mede so no dominio de producao. Previews do Vercel (*.vercel.app) e o servidor
// local de desenvolvimento nao configuram a medicao, entao nao sujam o GA4.
// Os eventos continuam sendo empilhados no dataLayer, o que permite testar sem enviar nada.
if (/(^|\.)livrosdofalco\.com\.br$/.test(location.hostname)) {
  gtag('config', 'G-R2ZQZ51DEK');

  // Microsoft Clarity: heatmap, rolagem e gravacao de sessao. Fica DENTRO do
  // mesmo guard do GA4 de proposito: preview e dev local nao podem gerar
  // sessao gravada, senao o heatmap conta os nossos proprios cliques de teste.
  (function(c,l,a,r,i,t,y){
      c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
      t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
      y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
  })(window, document, "clarity", "script", "y7n2in2vy0");
}

var RE_ASIN = /\/(?:dp|gp\/product)\/([A-Z0-9]{10})/;

// A pagina inteira aponta pra um unico ASIN? Se sim, ela e uma PDP e o <h1>
// dela E o titulo da obra. Se aponta pra varios (home, categoria, LP), o <h1>
// e o titulo DA PAGINA e nao serve. Calculado uma vez e guardado, porque nao
// muda depois que o DOM carrega.
var _umaObraSo = null;
function paginaDeUmaObraSo() {
  if (_umaObraSo !== null) return _umaObraSo;
  var vistos = {}, n = 0;
  var links = document.querySelectorAll('a[href*="/dp/"], a[href*="/gp/product/"]');
  for (var i = 0; i < links.length; i++) {
    var m = links[i].href.match(RE_ASIN);
    if (m && !vistos[m[1]]) { vistos[m[1]] = 1; n++; }
  }
  _umaObraSo = (n === 1);
  return _umaObraSo;
}

// Titulo da obra em degraus, do mais especifico pro mais generico:
//   1. h3 do card que envolve o link
//   2. aria-label do proprio link ("Comprar A Vila na Amazon" -> "A Vila")
//   3. alt da imagem dentro do link, cortado na 1a virgula
//   4. h1 da pagina, SO numa PDP (ver paginaDeUmaObraSo)
//   5. sem ASIN = link de busca do autor, nao e produto nenhum
//
// O degrau 4 antes era incondicional, e por isso a home mandava o proprio
// titulo dela ("Historias que Atravessam Seculos e Continentes") como se fosse
// obra: 18 de 96 cliques do mes, 18,8%, medido em 26/08/2026. O link do
// omnibus na home usa .omnibus-cover e nao .book-card, entao escapava do
// degrau 1 e caia direto no h1.
function tituloDaObra(link, asin) {
  // Sem ASIN nao e produto, e link de busca/loja do autor. Tem que sair antes
  // dos degraus de texto: o botao do catalogo tem aria-label "Ver catalogo
  // completo na Amazon", que viraria a "obra" chamada "catalogo completo".
  if (!asin) return '(loja Amazon)';

  var card = link.closest('.book-card');
  var h3 = card && card.querySelector('h3');
  if (h3 && h3.textContent.trim()) return h3.textContent.trim();

  var aria = link.getAttribute('aria-label');
  if (aria) {
    var limpo = aria.replace(/^\s*(?:comprar|ver|leia|conheça)\s+/i, '')
                    .replace(/\s+na\s+amazon\s*$/i, '')
                    .trim();
    if (limpo) return limpo;
  }

  var img = link.querySelector('img[alt]');
  if (img) {
    var alt = img.getAttribute('alt').split(',')[0].trim();
    if (alt) return alt;
  }

  var h1 = document.querySelector('h1');
  if (h1 && paginaDeUmaObraSo() && h1.textContent.trim()) return h1.textContent.trim();

  return '(sem titulo)';
}

document.addEventListener('click', function(e){
  if (typeof gtag !== 'function') return;
  var link = e.target.closest('a[href]');
  if (!link) return;
  var href = link.getAttribute('href') || '';

  // Casa pelo DOMINIO do link, nunca pelo href inteiro. Procurar "amazon" no
  // href contava o post /blog/desafios-expedicoes-floresta-amazonica/ como
  // saida para a loja (7 links internos apontam pra ele) e ainda engolia o
  // evento de teaser/nav do blog, porque o ramo faz "return".
  var saidaPara = function (re) { return re.test(link.hostname); };

  // O "(\.|$)" no fim cobre o encurtador oficial "link.amazon", cujo hostname
  // termina no proprio TLD .amazon e nao tem ponto depois.
  if (saidaPara(/(^|\.)(amazon|amzn)(\.|$)/)) {
    // obra_asin = ASIN tirado da propria URL. obra_titulo vem dos degraus de
    // tituloDaObra(), definida no topo do arquivo.
    // Os nomes NAO sao item_id/item_name de proposito: esses pertencem ao
    // namespace de e-commerce do GA4 e so populam relatorio de item dentro de
    // um evento de e-commerce. Aqui e clique de saida, entao viram dimensao
    // personalizada de escopo de evento com nome proprio.
    var asin = (link.href.match(RE_ASIN) || [])[1] || '';
    gtag('event', 'click_to_amazon', {
      event_category: 'saida_amazon',
      event_label: link.href,
      obra_asin: asin || '(sem asin)',
      obra_titulo: tituloDaObra(link, asin)
    });
    return;
  }
  if (saidaPara(/(^|\.)instagram\.com$/)) {
    gtag('event', 'click_instagram', { event_category: 'redes_sociais', event_label: link.href });
    return;
  }
  if (saidaPara(/(^|\.)tiktok\.com$/)) {
    gtag('event', 'click_tiktok', { event_category: 'redes_sociais', event_label: link.href });
    return;
  }
  if (saidaPara(/(^|\.)spotify\.com$/)) {
    gtag('event', 'click_spotify', { event_category: 'audiobook', event_label: link.href });
    return;
  }
  if (link.closest('.podcast-card')) {
    gtag('event', 'click_podcast_youtube', { event_category: 'audiobook', event_label: link.href });
    return;
  }
  if (href === '#sobre') {
    gtag('event', 'click_nav_sobre', { event_category: 'navegacao', event_label: 'sobre_autor' });
    return;
  }
  if (href === '#obras') {
    gtag('event', 'click_nav_obras', { event_category: 'navegacao', event_label: 'obras' });
    return;
  }
  if (link.classList.contains('cat-card')) {
    gtag('event', 'click_category_card', { event_category: 'categorias', event_label: href });
    return;
  }
  if (link.classList.contains('teaser-card')) {
    gtag('event', 'click_blog_teaser', { event_category: 'blog', event_label: href });
    return;
  }
  var personagemCard = link.closest('.character-card');
  if (personagemCard) {
    var foto = personagemCard.querySelector('.character-photo img');
    gtag('event', 'click_personagem', { event_category: 'personagens', event_label: foto && foto.alt ? foto.alt : href });
    return;
  }
  if (link.closest('.nav-dropdown-panel')) {
    gtag('event', 'click_nav_categorias', { event_category: 'navegacao', event_label: href });
    return;
  }
  if (href === '/categoria/' && link.closest('nav.links')) {
    gtag('event', 'click_nav_categorias', { event_category: 'navegacao', event_label: 'categorias_hub' });
    return;
  }
  if (href.indexOf('/blog') === 0 && link.closest('nav.links')) {
    gtag('event', 'click_nav_blog', { event_category: 'navegacao', event_label: 'blog_index' });
    return;
  }
});

// "play" nao borbulha (bubble) como clique, entao precisa de captura (useCapture=true)
// pra pegar o play de qualquer <audio> da pagina via um unico listener no document.
document.addEventListener('play', function(e){
  if (typeof gtag !== 'function') return;
  var audio = e.target;
  if (!audio || audio.tagName !== 'AUDIO') return;
  var card = audio.closest('.book-card');
  var label = card ? card.id : (audio.getAttribute('src') || '');
  gtag('event', 'play_audiobook_sample', { event_category: 'audiobook', event_label: label });
}, true);

// "toggle" do <details> tambem nao borbulha, mesma tecnica de captura do play acima.
// Registra so a ABERTURA: o que interessa e qual duvida a pessoa foi buscar.
// Fechar nao diz nada, e contar os dois inflaria o numero pela metade.
// Nao dispara no carregamento: o <details> que ja nasce aberto nao emite toggle.
document.addEventListener('toggle', function(e){
  if (typeof gtag !== 'function') return;
  var d = e.target;
  if (!d || d.tagName !== 'DETAILS' || !d.classList || !d.classList.contains('faq-item')) return;
  if (!d.open) return;
  var s = d.querySelector('summary');
  gtag('event', 'faq_open', {
    event_category: 'faq',
    event_label: s ? s.textContent.trim().slice(0, 100) : ''
  });
}, true);
