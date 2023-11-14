const produtosPorPagina = 6; // Número de produtos por página
let paginaAtual = 1; // Página atual

// ...

// Função para exibir produtos com base na página atual
function exibirProdutos() {
    const listaProdutos = document.getElementById('store');
    listaProdutos.innerHTML = ''; // Limpa a lista de produtos

    console.log("startIndex:", (paginaAtual - 1) * produtosPorPagina);
    console.log("endIndex:", startIndex + produtosPorPagina);

    for (let i = startIndex; i < endIndex && i < lista_produtos.length; i++) {
        const produto = lista_produtos[i];

        console.log("Exibindo produto:", produto);

        // Restante do código para criar elementos HTML
    }
}

// ...


// Atualize a paginação para refletir o número de páginas com base na quantidade de produtos
const totalPaginas = Math.ceil(lista_produtos.length / produtosPorPagina);
const paginacao = document.querySelector('.store-pagination');
paginacao.innerHTML = '';

const pages = Array.from({ length: totalPaginas }, (_, index) => index + 1);

for (const page of pages) {
    const itemPagina = document.createElement('li');
    itemPagina.innerHTML = `<a href="?page=${page}">${page}</a>`;
    if (page === paginaAtual) {
        itemPagina.classList.add('active');
    } else {
        itemPagina.addEventListener('click', function () {
            paginaAtual = page;
            exibirProdutos();
        });
    }
    paginacao.appendChild(itemPagina);
}

// Exiba os produtos iniciais
exibirProdutos();
