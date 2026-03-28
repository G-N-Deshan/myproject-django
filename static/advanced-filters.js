
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

    init() {
        this.loadFromURL();
        this.loadFromStorage();
        this.attachEventListeners();
        this.renderFilters();
        this.applyFilters();
    }

    loadFromURL() {
        const params = new URLSearchParams(window.location.search);

        if (params.has('min_price')) this.filters.minPrice = parseFloat(params.get('min_price'));
        if (params.has('max_price')) this.filters.maxPrice = parseFloat(params.get('max_price'));
        if (params.has('search')) this.filters.search = params.get('search');
        if (params.has('subcategory')) this.filters.category = params.get('subcategory');

        ['materials', 'sizes', 'brands'].forEach(key => {
            const values = params.getAll(key);
            if (values.length > 0) {
                this.filters[key] = values;
            }
        });
    }

    loadFromStorage() {
        try {
            const stored = localStorage.getItem(this.storageKey);
            if (stored) {
                const savedFilters = JSON.parse(stored);

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

    saveToStorage() {
        try {
            localStorage.setItem(this.storageKey, JSON.stringify(this.filters));
        } catch (error) {
            console.error('Error saving filters to storage:', error);
        }
    }

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

    setPriceRange(min, max) {
        this.filters.minPrice = min || null;
        this.filters.maxPrice = max || null;
        this.saveToStorage();
        this.updateURL();
    }

    toggleFilter(filterName, value) {
        this.updateFilter(filterName, value, true);
    }

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

        if (this.filters.minPrice) minInput.value = this.filters.minPrice;
        if (this.filters.maxPrice) maxInput.value = this.filters.maxPrice;

        minInput.addEventListener('input', updatePriceDisplay);
        maxInput.addEventListener('input', updatePriceDisplay);
    }

    renderFilterCheckboxes() {
        document.querySelectorAll('[data-filter-group]').forEach(checkbox => {
            const group = checkbox.dataset.filterGroup;
            const value = checkbox.dataset.filterValue;

            if (this.filters[group]?.includes(value)) {
                checkbox.checked = true;
            }

            checkbox.addEventListener('change', () => {
                this.toggleFilter(group, value);
                this.applyFilters();
            });
        });
    }

    renderFilters() {
        this.renderPriceSlider();
        this.renderFilterCheckboxes();
        this.updateFilterBadges();
    }

    updateFilterBadges() {
        const container = document.getElementById('active-filters-container');
        if (!container) return;

        const badges = [];

        if (this.filters.minPrice || this.filters.maxPrice) {
            const min = this.filters.minPrice || '0';
            const max = this.filters.maxPrice || '∞';
            badges.push({
                text: `$${min} - $${max}`,
                group: 'price'
            });
        }

        this.filters.materials.forEach(material => {
            badges.push({
                text: material,
                group: 'materials'
            });
        });

        this.filters.sizes.forEach(size => {
            badges.push({
                text: size,
                group: 'sizes'
            });
        });

        this.filters.brands.forEach(brand => {
            badges.push({
                text: brand,
                group: 'brands'
            });
        });

        if (badges.length > 0) {
            container.innerHTML = badges.map(badge => `
                <span class="filter-badge filter-badge-${badge.group}">
                    ${this.escapeHTML(badge.text)}
                    <button class="filter-badge-remove" data-group="${badge.group}" data-value="${this.escapeHTML(badge.text)}">
                        <i class="bi bi-x"></i>
                    </button>
                </span>
            `).join('');

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

    applyFilters() {
        const products = document.querySelectorAll('[data-product-id]');
        let visibleCount = 0;

        products.forEach(product => {
            let isVisible = true;

            if (this.filters.materials.length > 0) {
                const productMaterial = product.dataset.productMaterial || '';
                isVisible = isVisible && this.filters.materials.some(material =>
                    productMaterial.toLowerCase().includes(material.toLowerCase())
                );
            }

            if (this.filters.sizes.length > 0) {
                const productSizes = product.dataset.productSizes || '';
                isVisible = isVisible && this.filters.sizes.some(size =>
                    productSizes.toLowerCase().includes(size.toLowerCase())
                );
            }

            if (this.filters.brands.length > 0) {
                const productBrand = product.dataset.productBrand || '';
                isVisible = isVisible && this.filters.brands.some(brand =>
                    productBrand.toLowerCase().includes(brand.toLowerCase())
                );
            }

            product.style.display = isVisible ? 'block' : 'none';
            if (isVisible) visibleCount++;
        });

        this.showNoResultsMessage(visibleCount === 0);
    }

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

    attachEventListeners() {

        const clearBtn = document.getElementById('clear-all-filters-btn');
        if (clearBtn) {
            clearBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.clearAllFilters();
            });
        }

        document.querySelectorAll('[data-clear-group]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const group = btn.dataset.clearGroup;
                this.clearFilterGroup(group);

                this.updateFilterBadges();
                this.renderFilters();
            });
        });

        const filterPanel = document.getElementById('filter-panel');
        if (filterPanel && window.innerWidth < 768) {
            document.querySelectorAll('[data-filter-group]').forEach(checkbox => {
                checkbox.addEventListener('change', () => {

                    if (filterPanel.classList.contains('show')) {
                        filterPanel.classList.remove('show');
                    }
                });
            });
        }
    }

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

    getFilterState() {
        return { ...this.filters };
    }

    setFilterState(filters) {
        this.filters = { ...this.filters, ...filters };
        this.saveToStorage();
        this.updateURL();
        this.renderFilters();
        this.applyFilters();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.advancedFilters = new AdvancedFilters();
});
