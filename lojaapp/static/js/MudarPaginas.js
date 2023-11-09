const productsPerPage = 2; // Número de produtos por página
let currentPage = 1; // Página atual

// Função para exibir produtos com base na página atual
function displayProducts() {
   const productList = document.getElementById('product-list');
   productList.innerHTML = ''; // Limpa a lista de produtos

   const startIndex = (currentPage - 1) * productsPerPage;
   const endIndex = startIndex + productsPerPage;

   for (let i = startIndex; i < endIndex && i < listaProduto.length; i++) {
      const produto = listaProduto[i];
      // Crie os elementos HTML para exibir os produtos, por exemplo, divs, imagens, títulos, preços, etc., e adicione-os a productList.
   }
}

// Atualize a paginação para refletir o número de páginas com base na quantidade de produtos
const totalPages = Math.ceil(listaProduto.length / productsPerPage);
const storePagination = document.querySelector('.store-pagination');
storePagination.innerHTML = '';

for (let page = 1; page <= totalPages; page++) {
   const pageItem = document.createElement('li');
   pageItem.textContent = page;
   if (page === currentPage) {
      pageItem.classList.add('active');
   } else {
      pageItem.addEventListener('click', function () {
         currentPage = page;
         displayProducts();
      });
   }
   storePagination.appendChild(pageItem);
}
