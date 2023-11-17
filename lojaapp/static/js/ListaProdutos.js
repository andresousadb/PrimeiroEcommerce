document.addEventListener("DOMContentLoaded", function () {
    var checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', filterProducts);
    });

    function filterProducts() {
        var selectedCategories = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'))
            .map(function (checkbox) {
                return checkbox.getAttribute('data-category');
            });

        // Atualizar a URL com as categorias selecionadas
        var params = new URLSearchParams(window.location.search);
        params.set('categoria', selectedCategories.join(','));

        // Redirecionar para a nova URL
        window.location.href = '?' + params.toString();
    }

    // Chamar a função ao carregar a página
    updatePagination();

    // Função auxiliar para atualizar a paginação
    function updatePagination() {
        var paginationElement = document.getElementById('store-pagination');
        if (paginationElement) {
            var currentPage = parseInt(new URLSearchParams(window.location.search).get('page')) || 1;

            // Adapte esta parte para a lógica específica do seu aplicativo
            // Atualize os links de paginação com base na página atual
            // Certifique-se de usar a lógica correta para a paginação no carrinho
            // Aqui estou apenas imprimindo os valores no console
            console.log('Página atual:', currentPage);
            console.log('Lógica de paginação no carrinho...');

            // Remover os event listeners dos links de paginação existentes
            paginationElement.querySelectorAll('a').forEach(function (link) {
                link.removeEventListener('click', handlePaginationClick);
            });

            // Adicionar os event listeners novamente
            paginationElement.querySelectorAll('a').forEach(function (link) {
                link.addEventListener('click', handlePaginationClick);
            });
        }
    }

    // Função para lidar com o clique nos links de paginação
    function handlePaginationClick(event) {
        event.preventDefault();

        var page = event.target.getAttribute('data-page');
        if (page) {
            // Atualizar a URL com a nova página
            var params = new URLSearchParams(window.location.search);
            params.set('page', page);

            // Redirecionar para a nova URL
            window.location.href = '?' + params.toString();
        }
    }
});
