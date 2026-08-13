window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());

// Mede so no dominio de producao. Previews do Vercel (*.vercel.app) e o servidor
// local de desenvolvimento nao configuram a medicao, entao nao sujam o GA4.
// Os eventos continuam sendo empilhados no dataLayer, o que permite testar sem enviar nada.
if (/(^|\.)livrosdofalco\.com\.br$/.test(location.hostname)) {
  gtag('config', 'G-R2ZQZ51DEK');
}

document.addEventListener('click', function(e){
  if (typeof gtag !== 'function') return;
  var link = e.target.closest('a[href]');
  if (!link) return;
  var href = link.getAttribute('href') || '';

  if (link.href.indexOf('amazon') !== -1) {
    gtag('event', 'click_to_amazon', { event_category: 'saida_amazon', event_label: link.href });
    return;
  }
  if (link.href.indexOf('instagram.com') !== -1) {
    gtag('event', 'click_instagram', { event_category: 'redes_sociais', event_label: link.href });
    return;
  }
  if (link.href.indexOf('tiktok.com') !== -1) {
    gtag('event', 'click_tiktok', { event_category: 'redes_sociais', event_label: link.href });
    return;
  }
  if (link.href.indexOf('spotify.com') !== -1) {
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
