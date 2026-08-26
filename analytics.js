window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());

// ---------------------------------------------------------------------------
// Trafego interno: nao contar as nossas proprias visitas.
//
// A definicao por IP no admin do GA4 continua valendo, mas ela so cobre o
// escritorio. IP residencial e dinamico, o 4G do celular troca o tempo todo e o
// wi-fi da Bienal nao e nosso: toda visita fora daquele IP volta a ser contada
// como se fosse leitor. Esta marcacao resolve pelo navegador, que anda junto
// com a gente em vez de ficar preso a um endereco de rede.
//
// Ligar:    https://www.livrosdofalco.com.br/?interno=1
// Desligar: https://www.livrosdofalco.com.br/?interno=0
//
// Uma vez por navegador E por aparelho: a marca vive no localStorage, que nao
// atravessa janela anonima, outro navegador, outro celular, nem limpeza de
// dados do site. Depois de marcar, o parametro sai da URL sozinho, porque um
// link com "?interno=1" repassado por engano marcaria o leitor como se fosse a
// gente, e aquela pessoa sumiria do relatorio para sempre.
//
// O nome do parametro enviado e "traffic_type: internal", exatamente o mesmo
// que a definicao por IP usa. Assim o filtro de dados que ja existe no admin do
// GA4 pega os dois casos, sem configuracao nova.
// ---------------------------------------------------------------------------
var CHAVE_INTERNO = 'ldf_trafego_interno';

// localStorage estoura em navegador com dados de site bloqueados. O try/catch
// trata a falha como visitante normal: melhor contar uma visita nossa a mais do
// que derrubar a medicao de todo mundo por causa de uma excecao no topo do
// arquivo, que mataria tambem os eventos de clique la embaixo.
function marcaInterna(ligar) {
  try {
    if (ligar === undefined) return localStorage.getItem(CHAVE_INTERNO) === '1';
    if (ligar) localStorage.setItem(CHAVE_INTERNO, '1');
    else localStorage.removeItem(CHAVE_INTERNO);
    return ligar;
  } catch (e) { return false; }
}

var _pedido = (location.search.match(/[?&]interno=([^&#]*)/) || [])[1];
var trafegoMudou = _pedido !== undefined;
if (trafegoMudou) {
  marcaInterna(_pedido === '1' || _pedido === 'sim' || _pedido === 'true');
  // Limpa o ?interno= da barra de enderecos sem recarregar. Alem do link
  // repassado por engano, isso impede o GA4 de registrar "/?interno=1" como se
  // fosse uma pagina diferente da home.
  if (history.replaceState) {
    var _limpa = location.pathname +
      location.search.replace(/([?&])interno=[^&#]*(&|$)/, '$1').replace(/[?&]$/, '') +
      location.hash;
    history.replaceState(null, '', _limpa);
  }
}
var trafegoInterno = marcaInterna();

// Mede so no dominio de producao. Previews do Vercel (*.vercel.app) e o servidor
// local de desenvolvimento nao configuram a medicao, entao nao sujam o GA4.
// Os eventos continuam sendo empilhados no dataLayer, o que permite testar sem enviar nada.
if (/(^|\.)livrosdofalco\.com\.br$/.test(location.hostname)) {
  // O traffic_type vai no config, e nao num evento avulso: assim ele gruda em
  // TODOS os eventos da sessao, page_view incluido. Marcado so no clique, o GA4
  // continuaria contando a sessao e a pagina vista como se fossem de leitor.
  gtag('config', 'G-R2ZQZ51DEK', trafegoInterno ? { traffic_type: 'internal' } : {});

  // Microsoft Clarity: heatmap, rolagem e gravacao de sessao. Fica DENTRO do
  // mesmo guard do GA4 de proposito: preview e dev local nao podem gerar
  // sessao gravada, senao o heatmap conta os nossos proprios cliques de teste.
  // Visita marcada como interna fica de fora pela mesma razao.
  if (!trafegoInterno) {
    (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", "y7n2in2vy0");
  }
}

// Confirmacao visivel de que a marca pegou. Sem ela da pra marcar o celular,
// achar que funcionou, e so descobrir semanas depois que o numero continuou
// sujo, que e exatamente o problema que esta marcacao existe pra resolver.
// Aparece por 6 segundos, some sozinha, nao empurra layout (position:fixed) e e
// invisivel pra leitor de tela (aria-hidden), pra nao mexer na acessibilidade.
// Pra ver o aviso SO quando liga ou desliga, e nao em toda pagina, trocar a
// condicao abaixo por "if (!trafegoMudou) return;".
function avisaTrafegoInterno() {
  if (!trafegoInterno && !trafegoMudou) return;
  if (!document.body) return;
  var aviso = document.createElement('div');
  aviso.setAttribute('aria-hidden', 'true');
  aviso.textContent = trafegoInterno
    ? 'Tráfego interno LIGADO: esta visita não entra no GA4'
    : 'Tráfego interno DESLIGADO: esta visita volta a contar';
  aviso.style.cssText = 'position:fixed;left:12px;bottom:12px;z-index:2147483647;' +
    'max-width:80vw;padding:8px 12px;border-radius:6px;pointer-events:none;' +
    'font:600 12px/1.35 system-ui,-apple-system,sans-serif;color:#fff;' +
    'background:' + (trafegoInterno ? 'rgba(150,32,32,.93)' : 'rgba(28,92,54,.93)') + ';' +
    'box-shadow:0 2px 10px rgba(0,0,0,.35);transition:opacity .5s;';
  document.body.appendChild(aviso);
  setTimeout(function(){ aviso.style.opacity = '0'; }, 5500);
  setTimeout(function(){ if (aviso.parentNode) aviso.parentNode.removeChild(aviso); }, 6100);
}
// As duas paginas de /audiolivro/ carregam este arquivo sem defer, dentro do
// <head>, entao ali o body ainda nao existe quando o script roda.
if (document.body) avisaTrafegoInterno();
else document.addEventListener('DOMContentLoaded', avisaTrafegoInterno);

var RE_ASIN = /\/(?:dp|gp\/product)\/([A-Z0-9]{10})/;

// Titulo do JSON-LD do tipo Book. So a PDP declara Book; post de blog declara
// Article e a home nao declara nada. Esse e o unico jeito seguro de afirmar
// "a pagina INTEIRA e sobre esta obra", porque e o proprio site declarando.
// A versao anterior tentava adivinhar isso contando ASIN distinto na pagina, e
// errava no post de blog, que tambem aponta pra uma obra so: os 5 links de
// /blog/desafios-expedicoes-floresta-amazonica/ virariam uma "obra" chamada
// "Expedicoes na Amazonia: Desafios e Sobrevivencia". Sao 21 posts nessa
// situacao, ou seja, o bug da home so tinha mudado de endereco.
// Calculado uma vez e guardado: JSON-LD nao muda depois que a pagina carrega.
var _tituloBook;
function tituloDoBookSchema() {
  if (_tituloBook !== undefined) return _tituloBook;
  _tituloBook = '';
  var blocos = document.querySelectorAll('script[type="application/ld+json"]');
  for (var i = 0; i < blocos.length; i++) {
    var dados;
    try { dados = JSON.parse(blocos[i].textContent); } catch (e) { continue; }
    // Fila em vez de recursao: o schema pode vir como objeto, como array ou
    // embrulhado em @graph, e as tres formas aparecem no site.
    var fila = [].concat(dados);
    while (fila.length) {
      var no = fila.shift();
      if (!no || typeof no !== 'object') continue;
      if (no['@graph']) { fila = fila.concat(no['@graph']); continue; }
      if (no['@type'] === 'Book' && no.name) {
        _tituloBook = String(no.name).trim();
        return _tituloBook;
      }
    }
  }
  return _tituloBook;
}

// Titulo da obra em degraus, do mais especifico pro mais generico:
//   1. aria-label do proprio link ("Comprar A Vila na Amazon" -> "A Vila")
//   2. h3 do card que envolve o link
//   3. alt da imagem dentro do link, cortado na 1a virgula
//   4. name do JSON-LD Book, ou seja, a pagina e a PDP daquela obra
//   5. texto do proprio link, quando ele nomeia a obra
//   6. "(sem titulo)": o link nao carrega identidade nenhuma. Fica sem nome de
//      proposito. O obra_asin continua certo, entao o relatorio resolve o nome
//      pelo ASIN em vez de receber um titulo inventado, que foi exatamente o
//      erro que este arquivo esta consertando.
//
// O degrau do h1 da pagina saiu de vez. Era ele que fazia a home mandar o
// proprio titulo ("Historias que Atravessam Seculos e Continentes") como se
// fosse obra: 18 de 96 cliques do mes, 18,8%, medido em 26/08/2026. O link do
// omnibus na home usa .omnibus-cover e nao .book-card, entao escapava do
// degrau do card e caia direto no h1.
function tituloDaObra(link, asin) {
  // Sem ASIN nao e produto, e link de busca/loja do autor. Tem que sair antes
  // dos degraus de texto: o botao do catalogo tem aria-label "Ver catalogo
  // completo na Amazon", que viraria a "obra" chamada "catalogo completo".
  if (!asin) return '(loja Amazon)';

  // O aria-label vem antes do card de proposito: ele esta NO link, o h3 esta na
  // caixa em volta, e nem toda caixa fala da obra. Em /arquetipos/ os cards de
  // personagem reusam a classe .book-card e tem h3 com o nome do personagem,
  // entao o degrau do card mandava "John Storm", "Akira", "Dr. Carlos" e
  // "Dante" como se fossem titulos de obra desde que a LP subiu, em 21/08/2026.
  var aria = link.getAttribute('aria-label');
  if (aria) {
    var limpo = aria.replace(/^\s*(?:comprar|ver|ler|leia|conheça)\s+/i, '')
                    .replace(/\s+na\s+amazon\s*$/i, '')
                    .trim();
    if (limpo) return limpo;
  }

  var card = link.closest('.book-card');
  var h3 = card && card.querySelector('h3');
  if (h3 && h3.textContent.trim()) return h3.textContent.trim();

  var img = link.querySelector('img[alt]');
  if (img) {
    var alt = img.getAttribute('alt').split(',')[0].trim();
    if (alt) return alt;
  }

  var book = tituloDoBookSchema();
  if (book) return book;

  // Texto do proprio link. E o caso dos 21 posts do blog, que citam a obra no
  // meio da frase: "...serve de cenario para a epica obra <a>O Explorador</a>".
  // Vem depois do schema Book de proposito: na PDP o botao diz "Comece a lenda
  // agora", que nao e titulo de nada, e o schema resolve antes de chegar aqui.
  // O filtro de "amazon" derruba texto generico: "Ler na Amazon" perde o verbo
  // e o sufixo, mas se ainda sobrar "amazon" no meio, nao era titulo.
  var texto = (link.textContent || '').replace(/\s+/g, ' ').trim()
                 .replace(/^(?:comprar|ver|ler|leia|conheça)\s+/i, '')
                 .replace(/\s+na\s+amazon\s*$/i, '')
                 .replace(/[\s→>»·|-]+$/, '')
                 .trim();
  if (texto && texto.length <= 80 && !/amazon/i.test(texto)) return texto;

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
