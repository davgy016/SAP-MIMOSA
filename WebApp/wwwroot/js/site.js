

// Animate logo for only 10 seconds on first page load
window.addEventListener('DOMContentLoaded', function () {
    // Select all wave-letter and wave-arrow elements
    var waveLetters = document.querySelectorAll('.wave-letter');
    var waveArrows = document.querySelectorAll('.wave-arrow');

    // Add a class to enable animation
    waveLetters.forEach(function (el) { el.classList.add('wave-animate'); });
    waveArrows.forEach(function (el) { el.classList.add('wave-animate'); });

    // After 10 seconds, remove the animation class
    setTimeout(function () {
        waveLetters.forEach(function (el) { el.classList.remove('wave-animate'); });
        waveArrows.forEach(function (el) { el.classList.remove('wave-animate'); });
    }, 10000);
});

//Display tooltips

document.addEventListener('DOMContentLoaded', function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
