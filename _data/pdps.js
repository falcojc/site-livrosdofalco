// As obras que viram pagina no build de agora.
//
// O manifesto (_data/obras.json) tem as 32 obras do catalogo; esta lista tem
// so as que estao "prontas": conteudo escrito, ASIN, capa de PDP e um numero de
// onda no manifesto. Publicar as 30 de uma vez e o padrao que o Google trata
// como doorway, e a fila de indexacao deste site ja esta cheia, por isso a
// publicacao e por ondas e quem decide a onda e o manifesto, nao o template.
//
// Para subir a onda seguinte: preencher .claude/pdp/conteudo/{slug}.json com
// "onda": 1 e rodar `python .claude/pdp/gerar_manifesto.py --para-site`.
const obras = require("./obras.json");

module.exports = () => obras.filter((o) => o.pronta);
