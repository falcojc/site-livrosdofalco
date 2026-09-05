module.exports = function (eleventyConfig) {
  // Paginas e assets que ja existem hoje em producao — copia identica, sem
  // passar pelo motor de template (evita qualquer risco de interpretar
  // {{ }} / {% %} que porventura exista no HTML/JS ja publicado).
  eleventyConfig.addPassthroughCopy("index.html");
  // A pagina /o-mestre-das-tormentas passou a ser gerada pelo motor de PDP
  // (obra.njk). Aqui fica so a midia dela, que os blocos extras usam.
  eleventyConfig.addPassthroughCopy("o-mestre-das-tormentas/media");
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


  // ------------------------------------------------------------------ PDPs
  // Motor de PDP: uma pagina por obra, gerada a partir de _data/obras.json.
  // O manifesto nasce de `python .claude/pdp/gerar_manifesto.py --para-site`,
  // que funde o catalogo do EPUB, os ASINs canonicos e o conteudo escrito a mao.
  const OBRAS_PDP = require("./_data/obras.json");
  const SITE = "https://www.livrosdofalco.com.br";
  const TAG_AFILIADO = "falcojc-20";

  // Link da Amazon com a tag de afiliado e o rastro de origem. O ascsubtag e o
  // que separa, no relatorio do Associates, o clique que veio da PDP do clique
  // que veio da pagina de categoria.
  eleventyConfig.addFilter("linkAmazon", function (obra, origem) {
    const sub = "pdp-" + obra.slug_url + (origem ? "-" + origem : "");
    return "https://www.amazon.com.br/dp/" + obra.asin + "?tag=" + TAG_AFILIADO + "&ascsubtag=" + sub;
  });

  // Para onde aponta um link de obra. Se a obra ja tem PDP no ar, vai para ela;
  // se ainda nao tem, vai para a ancora dela na pagina de categoria, que e o
  // destino que existe hoje. Assim o bloco "se voce gostou deste" funciona
  // durante as ondas, sem link quebrado nem link para pagina inexistente.
  eleventyConfig.addFilter("urlObra", function (slug) {
    const o = OBRAS_PDP.find((x) => x.slug === slug || x.slug_url === slug);
    if (!o) return null;
    return o.pronta ? "/" + o.slug_url + "/" : o.ancora;
  });

  eleventyConfig.addFilter("obraPorSlug", function (slug) {
    return OBRAS_PDP.find((x) => x.slug === slug || x.slug_url === slug) || null;
  });

  eleventyConfig.addFilter("postPorSlug", function (posts, slug) {
    return (posts || []).find((p) => p.fileSlug === slug) || null;
  });

  // Dado estruturado da obra: Book + Offer + BreadcrumbList + FAQPage num grafo
  // so. Tres regras que valem ouro aqui:
  //   1. aggregateRating so sai quando existe avaliacao de verdade na Amazon.
  //      Emitir nota falsa e violacao de politica e rende acao manual.
  //   2. ASIN nao e ISBN nem GTIN. Ele entra como identifier/PropertyValue,
  //      que e o campo correto para codigo proprietario de loja.
  //   3. o preco so vira Offer quando esta no manifesto, conferido na loja.
  eleventyConfig.addFilter("jsonldObra", function (obra) {
    const url = SITE + "/" + obra.slug_url + "/";
    const imagem = SITE + (obra.capa_pdp ? obra.capa_pdp + "-800w.jpg" : obra.capa);
    const descricao = obra.descricao_seo || obra.gancho || "";

    const livro = {
      "@type": "Book",
      "@id": url + "#book",
      name: obra.titulo,
      author: { "@type": "Person", name: "Domenico Falco" },
      publisher: { "@type": "Organization", name: "Livros do Falco" },
      inLanguage: "pt-BR",
      genre: "Ficção Histórica",
      bookFormat: "https://schema.org/EBook",
      description: descricao,
      image: imagem,
      url: url,
      identifier: { "@type": "PropertyValue", propertyID: "ASIN", value: obra.asin },
    };
    if (obra.paginas) livro.numberOfPages = obra.paginas;
    if (obra.publicado) livro.datePublished = obra.publicado;
    if (obra.serie && obra.serie.nome) {
      livro.isPartOf = { "@type": "BookSeries", name: obra.serie.nome };
      if (obra.serie.parte) livro.position = obra.serie.parte;
    }
    if (obra.preco) {
      const validade = new Date();
      validade.setDate(validade.getDate() + 180);
      livro.offers = {
        "@type": "Offer",
        price: obra.preco.replace(".", "").replace(",", "."),
        priceCurrency: "BRL",
        priceValidUntil: validade.toISOString().split("T")[0],
        availability: "https://schema.org/InStock",
        url: "https://www.amazon.com.br/dp/" + obra.asin,
        seller: { "@type": "Organization", name: "Amazon.com.br" },
      };
    }
    if (obra.avaliacoes && obra.avaliacoes.total) {
      livro.aggregateRating = {
        "@type": "AggregateRating",
        ratingValue: obra.avaliacoes.nota,
        reviewCount: obra.avaliacoes.total,
      };
    }

    const trilha = [
      { "@type": "ListItem", position: 1, name: "Início", item: SITE + "/" },
    ];
    if (obra.silo) {
      trilha.push({
        "@type": "ListItem", position: 2, name: obra.silo_nome || obra.silo,
        item: SITE + "/categoria/" + obra.silo + "/",
      });
    }
    trilha.push({ "@type": "ListItem", position: trilha.length + 1, name: obra.titulo, item: url });

    const grafo = [livro, { "@type": "BreadcrumbList", itemListElement: trilha }];

    if (obra.faq && obra.faq.length) {
      grafo.push({
        "@type": "FAQPage",
        mainEntity: obra.faq.map((f) => ({
          "@type": "Question",
          name: f.p,
          acceptedAnswer: { "@type": "Answer", text: f.r },
        })),
      });
    }
    return JSON.stringify({ "@context": "https://schema.org", "@graph": grafo });
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
