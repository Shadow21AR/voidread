document.addEventListener('DOMContentLoaded', () => {
    const tocGrid = document.getElementById('tocGrid');
    const toggleButton = document.querySelector('.toc-toggle');
    const tocIcon = toggleButton.querySelector('.toc-icon');
    const tocLinks = tocGrid.querySelectorAll('a');

    let isTOCVisible = false;

    function toggleTOC() {
        isTOCVisible = !isTOCVisible;
        tocGrid.style.display = isTOCVisible ? 'grid' : 'none';
        toggleButton.setAttribute('aria-expanded', isTOCVisible);
        tocIcon.innerHTML = isTOCVisible
            ? '<i class="fas fa-chevron-up"></i>'
            : '<i class="fas fa-chevron-down"></i>';
    }

    toggleButton.addEventListener('click', toggleTOC);

    tocLinks.forEach(link => {
        link.addEventListener('click', () => {
            tocLinks.forEach(l => l.removeAttribute('aria-current'));
            link.setAttribute('aria-current', 'true');
            tocGrid.style.display = 'none';
            isTOCVisible = false;
            toggleButton.setAttribute('aria-expanded', false);
            tocIcon.innerHTML = '<i class="fas fa-chevron-down"></i>';
        });
    });

    // Initial icon
    tocIcon.innerHTML = '<i class="fas fa-chevron-down"></i>';
    tocGrid.style.display = 'none';

    // Optional: highlight section if URL has hash on load
    if (window.location.hash) {
        const hash = window.location.hash.toLowerCase();
        tocLinks.forEach(link => {
            if (link.getAttribute('href').toLowerCase() === hash) {
                link.setAttribute('aria-current', 'true');
            }
        });
    }
});