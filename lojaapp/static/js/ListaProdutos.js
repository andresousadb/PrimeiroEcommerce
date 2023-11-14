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

        console.log('Selected Categories:', selectedCategories);

        var products = document.querySelectorAll('.product-item');
        products.forEach(function (product) {
            var productCategory = product.dataset.category;

            console.log('Checking product:', productCategory);

            var isVisible = selectedCategories.length === 0 || selectedCategories.includes(productCategory);

            console.log('Product visibility:', isVisible);

            product.style.display = isVisible ? 'block' : 'none';
        });
    }
});
