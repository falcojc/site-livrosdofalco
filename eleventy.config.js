module.exports = function (eleventyConfig) {
  // Paginas e assets que ja existem hoje em producao — copia identica, sem
  // passar pelo motor de template (evita qualquer risco de interpretar
  // {{ }} / {% %} que porventura exista no HTML/JS ja publicado).
  eleventyConfig.addPassthroughCopy("index.html");
  eleventyConfig.addPassthroughCopy("o-mestre-das-tormentas");
  eleventyConfig.addPassthroughCopy("newsletter");
  eleventyConfig.addPassthroughCopy("covers");
  eleventyConfig.addPassthroughCopy("*.png");
  eleventyConfig.addPassthroughCopy("*.jpg");
  eleventyConfig.addPassthroughCopy("*.ico");
  eleventyConfig.addPassthroughCopy("SEO.txt");
  eleventyConfig.addPassthroughCopy("sitemap.xml");

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
