// Search Page JavaScript

function performSearch() {
    const query = document.getElementById('searchQuery').value.trim();
    
    if (!query) {
        alert('Iltimos, qidiruv so\'zini kiriting!');
        return;
    }
    
    // Simulated search - in real app, this would be an API call
    console.log('Searching for:', query);
    
    // Update result count
    document.getElementById('resultCount').textContent = '127';
    
    // Here you would typically make an AJAX call to Django backend
    // Example:
    // fetch(`/api/search/?q=${encodeURIComponent(query)}`)
    //     .then(response => response.json())
    //     .then(data => displayResults(data));
}

function displayResults(data) {
    const container = document.getElementById('resultsContainer');
    container.innerHTML = '';
    
    data.results.forEach(result => {
        const resultDiv = document.createElement('div');
        resultDiv.className = 'kwic-result';
        resultDiv.innerHTML = `
            <div class="kwic-context">
                <span class="kwic-left">${result.leftContext}</span>
                <span class="kwic-keyword">${result.keyword}</span>
                <span class="kwic-right">${result.rightContext}</span>
            </div>
            <div class="kwic-meta">
                <span class="source-title">${result.title}</span>
                <span class="source-author">${result.author}</span>
                <span class="source-year">${result.year}</span>
            </div>
        `;
        container.appendChild(resultDiv);
    });
}

// Search on Enter key
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchQuery');
    if (searchInput) {
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    }
});