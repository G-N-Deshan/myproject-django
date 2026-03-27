/**
 * Navbar Live Search
 * Provides real-time search suggestions as user types
 */

(function() {
    'use strict';
    
    const searchInput = document.getElementById('nav-search-input');
    const resultsContainer = document.getElementById('nav-search-results');
    const itemsContainer = document.getElementById('nav-search-items');
    const emptyMessage = document.getElementById('nav-search-empty');
    const spinner = document.getElementById('nav-search-spinner');
    
    let searchTimeout;
    const DEBOUNCE_DELAY = 300; // milliseconds
    const MIN_CHARS = 2; // Minimum characters to start searching
    
    if (!searchInput) return; // Exit if search input not found
    
    /**
     * Perform search via API
     */
    async function performSearch(query) {
        if (query.length < MIN_CHARS) {
            resultsContainer.style.display = 'none';
            return;
        }
        
        // Show spinner
        spinner.style.display = 'block';
        itemsContainer.innerHTML = '';
        emptyMessage.style.display = 'none';
        resultsContainer.style.display = 'block';
        
        try {
            const response = await fetch(`/api/products/?q=${encodeURIComponent(query)}&type=all`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            });
            
            if (!response.ok) throw new Error('Search failed');
            
            const data = await response.json();
            spinner.style.display = 'none';
            
            // Limit to first 6 results
            const results = data.products.slice(0, 6);
            
            if (results.length === 0) {
                emptyMessage.style.display = 'block';
                itemsContainer.innerHTML = '';
                return;
            }
            
            // Build results HTML
            itemsContainer.innerHTML = results.map(item => `
                <a href="${item.url}" class="nav-search-item" style="
                    display: flex;
                    align-items: center;
                    padding: 0.75rem;
                    border-bottom: 1px solid #f1f5f9;
                    text-decoration: none;
                    color: #1e293b;
                    transition: background 0.2s;
                    cursor: pointer;
                ">
                    <div style="
                        width: 50px;
                        height: 50px;
                        background: linear-gradient(135deg, #ede9fe, #e0e7ff);
                        border-radius: 8px;
                        margin-right: 0.75rem;
                        flex-shrink: 0;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        overflow: hidden;
                    ">
                        ${item.image ? `<img src="${item.image}" alt="${item.name}" style="width:100%;height:100%;object-fit:cover">` : '<span style="font-size:1.5rem">🛍️</span>'}
                    </div>
                    <div style="flex: 1; min-width: 0">
                        <div style="
                            font-weight: 500;
                            color: #1e293b;
                            white-space: nowrap;
                            overflow: hidden;
                            text-overflow: ellipsis;
                        ">${item.name}</div>
                        <div style="
                            font-size: 0.8rem;
                            color: #64748b;
                            margin-top: 0.2rem;
                        ">${item.type || 'Product'}</div>
                    </div>
                    <div style="
                        font-weight: 600;
                        color: #6366f1;
                        margin-left: 0.5rem;
                        white-space: nowrap;
                    ">Rs. ${item.price}</div>
                </a>
            `).join('');
            
            // Add hover effect
            document.querySelectorAll('.nav-search-item').forEach(item => {
                item.addEventListener('mouseenter', function() {
                    this.style.background = '#f8fafc';
                });
                item.addEventListener('mouseleave', function() {
                    this.style.background = 'transparent';
                });
            });
            
        } catch (error) {
            console.error('Search error:', error);
            spinner.style.display = 'none';
            emptyMessage.style.display = 'block';
            emptyMessage.textContent = 'Error loading results';
        }
    }
    
    /**
     * Debounced search handler
     */
    function handleSearchInput(e) {
        const query = e.target.value.trim();
        
        // Clear previous timeout
        clearTimeout(searchTimeout);
        
        if (!query) {
            resultsContainer.style.display = 'none';
            return;
        }
        
        // Set new timeout
        searchTimeout = setTimeout(() => {
            performSearch(query);
        }, DEBOUNCE_DELAY);
    }
    
    /**
     * Close dropdown when clicking outside
     */
    function handleClickOutside(e) {
        if (!e.target.closest('.nav-search-form')) {
            resultsContainer.style.display = 'none';
        }
    }
    
    /**
     * Handle keyboard navigation
     */
    function handleKeyDown(e) {
        if (e.key === 'Escape') {
            resultsContainer.style.display = 'none';
            searchInput.blur();
        } else if (e.key === 'Enter') {
            // Allow form submission
            return;
        }
    }
    
    // Event listeners
    searchInput.addEventListener('input', handleSearchInput);
    searchInput.addEventListener('keydown', handleKeyDown);
    searchInput.addEventListener('focus', function() {
        if (this.value.trim().length >= MIN_CHARS) {
            resultsContainer.style.display = 'block';
        }
    });
    
    document.addEventListener('click', handleClickOutside);
    
    // Close dropdown when a result is clicked
    document.addEventListener('click', function(e) {
        if (e.target.closest('.nav-search-item')) {
            // Allow navigation to happen naturally
            setTimeout(() => {
                resultsContainer.style.display = 'none';
            }, 100);
        }
    });
    
    console.log('✓ Navbar live search initialized');
})();
