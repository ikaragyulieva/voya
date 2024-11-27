// Show loader on page load and hide content
document.addEventListener("DOMContentLoaded", function () {
    const loader = document.getElementsByClassName("loader-wrapper")[0];
    const content = document.getElementsByTagName("main")[0];

    // Show loader and hide content initially
    loader.style.display = "flex";
    content.style.display = "none";

    // Once the page is fully loaded, hide the loader and show content
    window.addEventListener("load", function () {
        loader.style.display = "none";
        content.style.display = "flex";
    });
});