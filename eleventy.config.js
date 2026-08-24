module.exports = function (eleventyConfig) {
  // Paginas e assets que ja existem hoje em producao — copia identica, sem
  // passar pelo motor de template (evita qualquer risco de interpretar
  // {{ }} / {% %} que porventura exista no HTML/JS ja publicado).
  eleventyConfig.addPassthroughCopy("index.html");
  eleventyConfig.addPassthroughCopy("o-mestre-das-tormentas");
  eleventyConfig.addPassthroughCopy("newsletter");
  eleventyConfig.addPassthroughCopy("audiolivro");
  eleventyConfig.addPassthroughCopy("arquetipos");
  eleventyConfig.addPassthroughCopy("romance-historico");
  eleventyConfig.addPassthroughCopy("fonts");
  eleventyConfig.addPassthroughCopy("covers");
  eleventyConfig.addPassthroughCopy("personagens");
  eleventyConfig.addPassthroughCopy("banners");
  eleventyConfig.addPassthroughCopy("categoria");
  eleventyConfig.addPassthroughCopy("audio");
  // Imagens usadas nos e-mails da Brevo: elas precisam ter URL publica no
  // dominio, porque cliente de e-mail nao le arquivo local.
  eleventyConfig.addPassthroughCopy("email");
  eleventyConfig.addPassthroughCopy("*.png");
  eleventyConfig.addPassthroughCopy("*.jpg");
  eleventyConfig.addPassthroughCopy("*.webp");
  eleventyConfig.addPassthroughCopy("*.ico");
  eleventyConfig.addPassthroughCopy("SEO.txt");
  eleventyConfig.addPassthroughCopy("robots.txt");
  eleventyConfig.addPassthroughCopy("llms.txt");
  eleventyConfig.addPassthroughCopy("analytics.js");

  // Assets novos do blog (imagens de post, quando existirem)
  eleventyConfig.addPassthroughCopy({ "blog/posts/media": "blog/media" });

  // Flag de monetizacao: os slots de anuncio ja existem no template do post,
  // mas so renderizam de verdade quando isso virar true (pos-aprovacao do AdSense).
  eleventyConfig.addGlobalData("adsEnabled", false);

  // Posts com "draft: true" continuam sendo construidos (URL acessivel pra
  // revisao), mas ficam de fora do indice/RSS ate o rascunho ser publicado.
  // Nota: "tags" e aditivo no data cascade do Eleventy (nao da pra "zerar"
  // com tags:[] no front matter do post) — por isso o filtro e feito aqui,
  // por draft, em vez de depender de remover a tag "post".
  eleventyConfig.addCollection("post", function (collectionApi) {
    return collectionApi.getFilteredByTag("post").filter((item) => !item.data.draft);
  });

  // Carrossel de destaque da home do blog: curadoria manual via "heroOrder"
  // no front matter (nunca posts com draft:true, mesmo que tenham heroOrder).
  eleventyConfig.addCollection("hero", function (collectionApi) {
    return collectionApi
      .getFilteredByTag("post")
      .filter((item) => !item.data.draft && item.data.heroOrder)
      .sort((a, b) => a.data.heroOrder - b.data.heroOrder);
  });

  eleventyConfig.addFilter("readingTime", function (content) {
    const text = String(content).replace(/<[^>]*>/g, " ");
    const words = text.trim().split(/\s+/).filter(Boolean).length;
    return Math.max(1, Math.round(words / 200));
  });

  eleventyConfig.addFilter("dateBR", function (dateObj) {
    return new Date(dateObj).toLocaleDateString("pt-BR", {
      day: "numeric", month: "long", year: "numeric", timeZone: "UTC"
    });
  });

  eleventyConfig.addFilter("dateISO", function (dateObj) {
    return new Date(dateObj).toISOString().split("T")[0];
  });

  eleventyConfig.addFilter("isExternal", function (url) {
    return typeof url === "string" && url.indexOf("http") === 0;
  });

  // Imagens do corpo do post viram figure+figcaption (legenda visivel usando
  // o proprio alt text), em vez de <img> solto dentro de um <p>.
  eleventyConfig.amendLibrary("md", (mdLib) => {
    const escapeHtml = mdLib.utils.escapeHtml;
    mdLib.renderer.rules.image = function (tokens, idx) {
      const token = tokens[idx];
      const src = token.attrGet("src");
      const alt = escapeHtml(token.content);
      return `<figure class="post-figure"><img src="${src}" alt="${alt}" loading="lazy"><figcaption>${alt}</figcaption></figure>`;
    };
  });

  return {
    dir: {
      input: ".",
      includes: "_includes",
      output: "_site"
    },
    templateFormats: ["njk", "md"],
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk"
  };
};
