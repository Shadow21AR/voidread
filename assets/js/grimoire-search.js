document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('searchInput');
    const clearBtn = document.getElementById('clearSearch');
    const loader = document.getElementById('searchLoader');
    const overlay = document.getElementById('searchOverlay');
    const content = document.querySelectorAll('#main h2, #main h3, #main h4, #main p, #main li');

    let currentIndex = -1;
    let results = [];

    function getVisibleText(el) {
        let text = '';
        for (const node of el.childNodes) {
            if (node.nodeType === Node.TEXT_NODE) {
                text += node.textContent;
            } else if (node.nodeType === Node.ELEMENT_NODE && !node.classList.contains('header-link')) {
                text += getVisibleText(node);
            }
        }
        return text.trim();
    }

    function clearSearch() {
        input.value = '';
        overlay.innerHTML = '';
        overlay.style.display = 'none';
        loader.style.display = 'none';
        currentIndex = -1;
    }

    clearBtn.addEventListener('click', clearSearch);

    document.addEventListener('keydown', e => {
        if (e.key === 'Escape') clearSearch();
        if (e.ctrlKey && e.key.toLowerCase() === 'f') {
            e.preventDefault();
            input.focus();
        }
        if (overlay.style.display === 'block') {
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                setActive(currentIndex + 1);
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                setActive(currentIndex - 1);
            } else if (e.key === 'Enter' && results[currentIndex]) {
                results[currentIndex].el.scrollIntoView({ behavior: 'smooth', block: 'center' });
                clearSearch();
            }
        }
    });

    function setActive(index) {
        if (results.length === 0) return;
        if (results[currentIndex]) results[currentIndex].node.classList.remove('active');
        currentIndex = (index + results.length) % results.length;
        results[currentIndex].node.classList.add('active');
        results[currentIndex].node.scrollIntoView({ block: 'nearest' });
    }

    input.addEventListener('input', () => {
        const query = input.value.trim().toLowerCase();
        overlay.innerHTML = '';
        overlay.style.display = 'none';
        currentIndex = -1;

        if (query.length <= 2) return;

        loader.style.display = 'block';

        const matches = Array.from(content)
            .filter(el => getVisibleText(el).toLowerCase().includes(query))
            .slice(0, 20);

        results = matches.map(match => {
            const text = getVisibleText(match);
            const regex = new RegExp(`(${query})`, 'gi');
            const highlighted = text.replace(regex, '<span class="search-highlight">$1</span>');
            const div = document.createElement('div');
            div.className = 'search-result-block';
            div.innerHTML = highlighted;
            div.addEventListener('click', () => {
                match.scrollIntoView({ behavior: 'smooth', block: 'center' });
                clearSearch();
            });
            overlay.appendChild(div);
            return { node: div, el: match };
        });

        if (results.length) {
            overlay.style.display = 'block';
        } else {
            overlay.innerHTML = '<div class="search-result-block"><em>No results found.</em></div>';
            overlay.style.display = 'block';
        }

        loader.style.display = 'none';
    });
});