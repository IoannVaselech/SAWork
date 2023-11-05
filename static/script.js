// script.js

function showLoadingIndicator() {
    var loadingIndicator = document.getElementById("loading-indicator");
    loadingIndicator.style.display = "block";
}

function hideLoadingIndicator() {
    var loadingIndicator = document.getElementById("loading-indicator");
    loadingIndicator.style.display = "none";
}

function pageLoaded() {
    showLoadingIndicator();  // Показать индикатор загрузки при загрузке страницы
    // Здесь можете добавить другую логику, если необходимо
    // ...
}
