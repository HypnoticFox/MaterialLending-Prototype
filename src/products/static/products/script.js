if (document.readyState !== 'loading') {
    initCode();
} else {
    document.addEventListener('DOMContentLoaded', function () {
        initCode();
    });
}

function initCode() {
    initProductCategory();
}

function initProductCategory() {
    const urlParts = window.location.pathname.split('/').filter(x => x);
    const areaPart = urlParts[urlParts.length - 2];
    const urlEnd = urlParts[urlParts.length - 1];

    if(areaPart !== 'products' || urlEnd !== 'new') { return; }

    const categorySelect = document.querySelector('select[name="category"]');
    if(categorySelect != null) {
        const previousCategoryChoice = localStorage.getItem("scoutdepot-new-product-previous-category-choice");
        const availableCategories = [...categorySelect.options].map(x => x.value);

        if(previousCategoryChoice != null && availableCategories.includes(previousCategoryChoice)) {
            categorySelect.value = previousCategoryChoice;
        }

        categorySelect.addEventListener('change', (event) => {
            localStorage.setItem("scoutdepot-new-product-previous-category-choice", event.target.value);
        });
    }
}