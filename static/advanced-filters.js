/**
 * Advanced Filter System
 * Manages product filtering with persistence across page navigation
 * Supports: price range, materials, sizes, brands, categories
 */

class AdvancedFilters {
    constructor() {
        this.filters = {
            minPrice: null,
            maxPrice: null,
            materials: [],
            sizes: [],
            brands: [],
            category: null,
            search: '',
        };
        
        this.storageKey = 'advanced-filters';
        this.init();
    }
    
    /**
     * Initialize filters from URL parameters and localStorage
     */
    init() {
        this.loadFromURL();
        this.loadFromStorage();
        this.attachEventListeners();
        this.renderFilters();
        this.applyFilters();
    }
    
    /**
     * Load filters from URL query parameters
     */
    loadFromURL() {
        const params = new URLSearchParams(window.location.search);
        
        if (params.has('min_price')) this.filters.minPrice = parseFloat(params.get('min_price'));
        if (params.has('max_price')) this.filters.maxPrice = parseFloat(params.get('max_price'));
        if (params.has('search')) this.filters.search = params.get('search');
        if (params.has('subcategory')) this.filters.category = params.get('subcategory');
        
        // Load multiple values for arrays
        ['materials', 'sizes', 'brands'].forEach(key => {
            const values = params.getAll(key);
            if (values.length > 0) {
                this.filters[key] = values;
            }
        });
    }
    
    /**
     * Load filters from localStorage (overrides with URL if present)
     */
    loadFromStorage() {
        try {
            const stored = localStorage.getItem(this.storageKey);
            if (stored) {
                const savedFilters = JSON.parse(stored);
                // Only load non-URL filters from storage
                const params = new URLSearchParams(window.location.search);
                
                if (!params.has('min_price') && savedFilters.minPrice) {
                    this.filters.minPrice = savedFilters.minPrice;
                }
                if (!params.has('max_price') && savedFilters.maxPrice) {
                    this.filters.maxPrice = savedFilters.maxPrice;
                }
                if (!params.has('materials') && savedFilters.materials?.length) {
                    this.filters.materials = savedFilters.materials;
                }
                if (!params.has('sizes') && savedFilters.sizes?.length) {
                    this.filters.sizes = savedFilters.sizes;
                }
                if (!params.has('brands') && savedFilters.brands?.length) {
                    this.filters.brands = savedFilters.brands;
                }
            }
        } catch (error) {
            console.error('Error loading filters from storage:', error);
        }
    }
    
    /**
     * Save filters to localStorage
     */
    saveToStorage() {
        try {
            localStorage.setItem(this.storageKey, JSON.stringify(this.filters));
        } catch (error) {
            console.error('Error saving filters to storage:', error);
        }
    }
    
    /**
     * Update filter value
     */
    updateFilter(filterName, value, isArray = false) {
        if (isArray) {
            if (this.filters[filterName].includes(value)) {
                this.filters[filterName] = this.filters[filterName].filter(v => v !== value);
            } else {
                this.filters[filterName].push(value);
            }
        } else {
            this.filters[filterName] = value;
        }
        
        this.saveToStorage();
        this.updateURL();
    }
    
    /**
     * Set price range
     */
    setPriceRange(min, max) {
        this.filters.minPrice = min || null;
        this.filters.maxPrice = max || null;
        this.saveToStorage();
        this.updateURL();
    }
    
    /**
     * Toggle filter checkbox (material, size, brand)
     */
    toggleFilter(filterName, value) {
        this.updateFilter(filterName, value, true);
    }
    
    /**
     * Clear all filters
     */
    clearAllFilters() {
        this.filters = {
            minPrice: null,
            maxPrice: null,
            materials: [],
            sizes: [],
            brands: [],
            category: null,
            search: '',
        };
        this.saveToStorage();
        this.updateURL();
        window.location.reload();
    }
    
    /**
     * Clear specific filter group
     */
    clearFilterGroup(groupName) {
        if (groupName === 'price') {
            this.filters.minPrice = null;
            this.filters.maxPrice = null;
        } else if (Array.isArray(this.filters[groupName])) {
            this.filters[groupName] = [];
        }
        this.saveToStorage();
        this.updateURL();
    }
    
    /**
     * Update URL to reflect current filters (for bookmarking/sharing)
     */
    updateURL() {
        const base = window.location.pathname;
        const params = new URLSearchParams();
        
        if (this.filters.minPrice) params.append('min_price', this.filters.minPrice);
        if (this.filters.maxPrice) params.append('max_price', this.filters.maxPrice);
        if (this.filters.search) params.append('q', this.filters.search);
        if (this.filters.category) params.append('subcategory', this.filters.category);
        
        this.filters.materials.forEach(m => params.append('materials', m));
        this.filters.sizes.forEach(s => params.append('sizes', s));
        this.filters.brands.forEach(b => params.append('brands', b));
        
        const newURL = params.toString() ? `${base}?${params}` : base;
        window.history.replaceState(null, '', newURL);
    }
    
    /**
     * Render price slider UI
     */
    renderPriceSlider() {
        const container = document.getElementById('price-slider-container');
        if (!container) return;
        
        const minInput = container.querySelector('#price-min-slider');
        const maxInput = container.querySelector('#price-max-slider');
        const minDisplay = container.querySelector('[data-price-min]');
        const maxDisplay = container.querySelector('[data-price-max]');
        
        if (!minInput || !maxInput) return;
        
        const updatePriceDisplay = () => {
            const min = parseFloat(minInput.value);
            const max = parseFloat(maxInput.value);
            
            if (minDisplay) minDisplay.textContent = `$${min.toFixed(2)}`;
            if (maxDisplay) maxDisplay.textContent = `$${max.toFixed(2)}`;
            
            this.setPriceRange(min, max);
            this.applyFilters();
        };
        
        // Set initial values from filters
        if (this.filters.minPrice) minInput.value = this.filters.minPrice;
        if (this.filters.maxPrice) maxInput.value = this.filters.maxPrice;
        
        minInput.addEventListener('input', updatePriceDisplay);
        maxInput.addEventListener('input', updatePriceDisplay);
    }
    
    /**
     * Render filter checkboxes
     */
    renderFilterCheckboxes() {
        document.querySelectorAll('[data-filter-group]').forEach(checkbox => {
            const group = checkbox.dataset.filterGroup;
            const value = checkbox.dataset.filterValue;
            
            // Set checked state
            if (this.filters[group]?.includes(value)) {
                checkbox.checked = true;
            }
            
            // Add change listener
            checkbox.addEventListener('change', () => {
                this.toggleFilter(group, value);
                this.applyFilters();
            });
        });
    }
    
    /**
     * Render all filter UI elements
     */
    renderFilters() {
        this.renderPriceSlider();
        this.renderFilterCheckboxes();
        this.updateFilterBadges();
    }
    
    /**
     * Update active filter badges
     */
    updateFilterBadges() {
        const container = document.getElementById('active-filters-container');
        if (!container) return;
        
        const badges = [];
        
        // Price range badge
        if (this.filters.minPrice || this.filters.maxPrice) {
            const min = this.filters.minPrice || '0';
            const max = this.filters.maxPrice || '∞';
            badges.push({
                text: `$${min} - $${max}`,
                group: 'price'
            });
        }
        
        // Material badges
        this.filters.materials.forEach(material => {
            badges.push({
                text: material,
                group: 'materials'
            });
        });
        
        // Size badges
        this.filters.sizes.forEach(size => {
            badges.push({
                text: size,
                group: 'sizes'
            });
        });
        
        // Brand badges
        this.filters.brands.forEach(brand => {
            badges.push({
                text: brand,
                group: 'brands'
            });
        });
        
        // Render badges
        if (badges.length > 0) {
            container.innerHTML = badges.map(badge => `
                <span class="filter-badge filter-badge-${badge.group}">
                    ${this.escapeHTML(badge.text)}
                    <button class="filter-badge-remove" data-group="${badge.group}" data-value="${this.escapeHTML(badge.text)}">
                        <i class="bi bi-x"></i>
                    </button>
                </span>
            `).join('');
            
            // Add remove listeners
            container.querySelectorAll('.filter-badge-remove').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    e.preventDefault();
                    const group = btn.dataset.group;
                    const value = btn.dataset.value;
                    this.toggleFilter(group, value);
                    this.updateFilterBadges();
                    this.applyFilters();
                });
            });
            
            container.style.display = 'flex';
        } else {
            container.innerHTML = '';
            container.style.display = 'none';
        }
    }
    
    /**
     * Apply filters by filtering visible products (client-side)
     * This works with server-side filtered results
     */
    applyFilters() {
        const products = document.querySelectorAll('[data-product-id]');
        let visibleCount = 0;
        
        products.forEach(product => {
            let isVisible = true;
            
            // Filter by materials
            if (this.filters.materials.length > 0) {
                const productMaterial = product.dataset.productMaterial || '';
                isVisible = isVisible && this.filters.materials.some(material => 
                    productMaterial.toLowerCase().includes(material.toLowerCase())
                );
            }
            
            // Filter by sizes
            if (this.filters.sizes.length > 0) {
                const productSizes = product.dataset.productSizes || '';
                isVisible = isVisible && this.filters.sizes.some(size =>
                    productSizes.toLowerCase().includes(size.toLowerCase())
                );
            }
            
            // Filter by brands
            if (this.filters.brands.length > 0) {
                const productBrand = product.dataset.productBrand || '';
                isVisible = isVisible && this.filters.brands.some(brand =>
                    productBrand.toLowerCase().includes(brand.toLowerCase())
                );
            }
            
            // Apply visibility
            product.style.display = isVisible ? 'block' : 'none';
            if (isVisible) visibleCount++;
        });
        
        // Show "no results" message if needed
        this.showNoResultsMessage(visibleCount === 0);
    }
    
    /**
     * Show/hide "no results" message
     */
    showNoResultsMessage(show) {
        let message = document.getElementById('no-filters-results-message');
        
        if (show) {
            if (!message) {
                message = document.createElement('div');
                message.id = 'no-filters-results-message';
                message.className = 'no-results-message';
                message.innerHTML = `
                    <div class="no-results-content">
                        <i class="bi bi-search"></i>
                        <p>No products match your filters</p>
                        <button class="btn btn-outline-secondary" id="clear-filters-btn">
                            Clear Filters
                        </button>
                    </div>
                `;
                const container = document.querySelector('[data-products-container]') || 
                                 document.querySelector('.products-grid');
                if (container) {
                    container.parentElement.appendChild(message);
                    document.getElementById('clear-filters-btn').addEventListener('click', 
                        () => this.clearAllFilters());
                }
            }
            message.style.display = 'block';
        } else if (message) {
            message.style.display = 'none';
        }
    }
    
    /**
     * Attach event listeners to filter UI
     */
    attachEventListeners() {
        // Clear all filters button
        const clearBtn = document.getElementById('clear-all-filters-btn');
        if (clearBtn) {
            clearBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.clearAllFilters();
            });
        }
        
        // Clear filter group buttons
        document.querySelectorAll('[data-clear-group]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const group = btn.dataset.clearGroup;
                this.clearFilterGroup(group);
                // Update UI without reload if possible
                this.updateFilterBadges();
                this.renderFilters();
            });
        });
        
        // Hide filter panel on mobile when filter applied
        const filterPanel = document.getElementById('filter-panel');
        if (filterPanel && window.innerWidth < 768) {
            document.querySelectorAll('[data-filter-group]').forEach(checkbox => {
                checkbox.addEventListener('change', () => {
                    // Close panel after selection on mobile
                    if (filterPanel.classList.contains('show')) {
                        filterPanel.classList.remove('show');
                    }
                });
            });
        }
    }
    
    /**
     * Escape HTML to prevent XSS
     */
    escapeHTML(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }
    
    /**
     * Get current filter state (for exporting)
     */
    getFilterState() {
        return { ...this.filters };
    }
    
    /**
     * Apply filters from external source
     */
    setFilterState(filters) {
        this.filters = { ...this.filters, ...filters };
        this.saveToStorage();
        this.updateURL();
        this.renderFilters();
        this.applyFilters();
    }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    window.advancedFilters = new AdvancedFilters();
});
