// Log de trafego de IA. Roda no Edge da Vercel, antes de servir a pagina.
//
// Grava duas coisas na tabela `ai_traffic_log` do Supabase:
//   kind='crawl' -> um robo de IA veio raspar uma pagina (o custo)
//   kind='refer' -> um humano chegou vindo de um assistente de IA (o retorno)
// A razao entre as duas e o crawl-to-refer ratio.
//
// Nao grava IP, so pais (header da propria Vercel).
// Tudo dentro de try/catch: se o log falhar, a requisicao segue normal.

const SUPABASE_URL = 'https://nxyfrctnavkleusiuvsp.supabase.co';
const SUPABASE_KEY = 'sb_publishable_Pu5RG0UsGTg447l5u7AnvQ_ostSUQ3J';

// Quem raspa. Mais especifico primeiro (Applebot-Extended antes de Applebot).
const CRAWLERS = [
  ['GPTBot', 'openai'],
  ['OAI-SearchBot', 'openai'],
  ['ChatGPT-User', 'openai'],
  ['ClaudeBot', 'anthropic'],
  ['Claude-SearchBot', 'anthropic'],
  ['Claude-User', 'anthropic'],
  ['anthropic-ai', 'anthropic'],
  ['PerplexityBot', 'perplexity'],
  ['Perplexity-User', 'perplexity'],
  ['Google-Extended', 'google-ia'],
  ['Google-CloudVertexBot', 'google-ia'],
  ['Applebot-Extended', 'apple'],
  ['Applebot', 'apple'],
  ['meta-externalagent', 'meta'],
  ['meta-externalfetcher', 'meta'],
  ['FacebookBot', 'meta'],
  ['Bytespider', 'bytedance'],
  ['TikTokSpider', 'bytedance'],
  ['Amazonbot', 'amazon'],
  ['CCBot', 'commoncrawl'],
  ['cohere-ai', 'cohere'],
  ['MistralAI-User', 'mistral'],
  ['DuckAssistBot', 'duckduckgo'],
  ['YouBot', 'you'],
  ['Diffbot', 'diffbot'],
  ['ImagesiftBot', 'imagesift'],
  ['Timpibot', 'timpi'],
  ['omgili', 'webz'],
  ['AhrefsBot', 'seo'],
  ['SemrushBot', 'seo'],
  // Busca tradicional: e o denominador de comparacao. Googlebot alimenta tanto
  // o link azul quanto o AI Overview, por isso fica separado do Google-Extended.
  ['Googlebot', 'busca'],
  ['bingbot', 'busca'],
  ['DuckDuckBot', 'busca'],
  ['YandexBot', 'busca'],
];

// Quem devolve gente. Casado contra o referer e contra utm_source, porque
// varios assistentes abrem link com rel="noreferrer" e so deixam o utm.
const REFERRERS = [
  ['chatgpt.com', 'openai'],
  ['chat.openai.com', 'openai'],
  ['openai.com', 'openai'],
  ['perplexity.ai', 'perplexity'],
  ['claude.ai', 'anthropic'],
  ['gemini.google.com', 'google-ia'],
  ['bard.google.com', 'google-ia'],
  ['copilot.microsoft.com', 'microsoft'],
  ['edgeservices.bing.com', 'microsoft'],
  ['grok.com', 'xai'],
  ['x.ai', 'xai'],
  ['you.com', 'you'],
  ['poe.com', 'poe'],
  ['mistral.ai', 'mistral'],
  ['duckduckgo.com/aichat', 'duckduckgo'],
];

function detectar(ua, referer, utm) {
  const uaLower = ua.toLowerCase();
  for (let i = 0; i < CRAWLERS.length; i++) {
    if (uaLower.indexOf(CRAWLERS[i][0].toLowerCase()) !== -1) {
      return { kind: 'crawl', agent: CRAWLERS[i][0], vendor: CRAWLERS[i][1] };
    }
  }
  const alvo = (referer + ' ' + utm).toLowerCase();
  if (alvo.trim()) {
    for (let i = 0; i < REFERRERS.length; i++) {
      if (alvo.indexOf(REFERRERS[i][0]) !== -1) {
        return { kind: 'refer', agent: REFERRERS[i][0], vendor: REFERRERS[i][1] };
      }
    }
  }
  return null;
}

export const config = {
  // Ignora asset (imagem, fonte, css, audio): so interessa pagina e arquivo
  // de texto (robots.txt, llms.txt, sitemap.xml sao justamente o que robo pede).
  matcher: [
    '/((?!.*\.(?:png|jpg|jpeg|gif|webp|svg|ico|css|js|mjs|map|woff2|woff|ttf|otf|mp3|mp4|m4a|pdf)$).*)',
  ],
};

export default async function middleware(request, context) {
  try {
    const ua = request.headers.get('user-agent') || '';
    const referer = request.headers.get('referer') || '';
    const u = new URL(request.url);
    const utm =
      (u.searchParams.get('utm_source') || '') + ' ' + (u.searchParams.get('ref') || '');

    const hit = detectar(ua, referer, utm);
    if (hit) {
      const envio = fetch(SUPABASE_URL + '/rest/v1/ai_traffic_log', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          apikey: SUPABASE_KEY,
          Authorization: 'Bearer ' + SUPABASE_KEY,
          Prefer: 'return=minimal',
        },
        body: JSON.stringify({
          kind: hit.kind,
          agent: hit.agent,
          vendor: hit.vendor,
          path: u.pathname.slice(0, 300),
          ua: ua.slice(0, 400),
          referer: hit.kind === 'refer' ? referer.slice(0, 300) || null : null,
          country: request.headers.get('x-vercel-ip-country') || null,
        }),
      }).catch(function () {});

      if (context && typeof context.waitUntil === 'function') context.waitUntil(envio);
      else await envio;
    }
  } catch (e) {
    // Log e acessorio: nunca pode derrubar a pagina.
  }
  // Sem Response retornada, a requisicao segue para o destino normal.
}
