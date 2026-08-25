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
    // obra_asin = ASIN tirado da propria URL. obra_titulo segue tres degraus:
    // titulo do card que envolve o link, senao o <h1> da pagina (caso da PDP,
    // que nao tem card), senao "(loja Amazon)" pros links de busca de autor,
    // que nao sao produto nenhum e sujariam o relatorio com o titulo da home.
    // Os nomes NAO sao item_id/item_name de proposito: esses pertencem ao
    // namespace de e-commerce do GA4 e so populam relatorio de item dentro de
    // um evento de e-commerce. Aqui e clique de saida, entao viram dimensao
    // personalizada de escopo de evento com nome proprio.
    var asin = (link.href.match(/\/(?:dp|gp\/product)\/([A-Z0-9]{10})/) || [])[1] || '';
    var card = link.closest('.book-card');
    var titulo = card && card.querySelector('h3');
    var h1 = document.querySelector('h1');
    gtag('event', 'click_to_amazon', {
      event_category: 'saida_amazon',
      event_label: link.href,
      obra_asin: asin || '(sem asin)',
      obra_titulo: titulo ? titulo.textContent.trim()
                 : (asin && h1) ? h1.textContent.trim()
                 : '(loja Amazon)'
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
