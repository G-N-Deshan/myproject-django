/**
 * PRODUCT COMPARISON TOOL
 * Allows comparing 2-4 products side-by-side
 */

class ProductComparison {
    constructor() {
        this.maxComparisons = 4;
        this.comparisons = this.loadFromStorage();
        this.init();
    }

    init() {
        this.attachEventListeners();
        this.renderComparisonWidget();
    }

    /**
     * Load comparison list from localStorage
     */
    loadFromStorage() {
        const stored = localStorage.getItem('productComparisons');
        return stored ? JSON.parse(stored) : [];
    }

    /**
     * Save comparison list to localStorage
     */
    saveToStorage() {
        localStorage.setItem('productComparisons', JSON.stringify(this.comparisons));
        this.renderComparisonWidget();
    }

    /**
     * Add product to comparison
     */
    addProduct(itemType, itemId) {
        // Check if already in comparison
        if (this.comparisons.some(c => c.itemType === itemType && c.itemId === itemId)) {
            this.showToast(`Product already in comparison`, 'warning');
            return;
        }

        // Check max limit
        if (this.comparisons.length >= this.maxComparisons) {
            this.showToast(`Maximum ${this.maxComparisons} products can be compared`, 'warning');
            return;
        }

        this.comparisons.push({ itemType, itemId });
        this.saveToStorage();
        this.showToast('Added to comparison', 'success');
        this.updateComparisonButtons();
    }

    /**
     * Remove product from comparison
     */
    removeProduct(itemType, itemId) {
        this.comparisons = this.comparisons.filter(
            c => !(c.itemType === itemType && c.itemId === itemId)
        );
        this.saveToStorage();
        this.showToast('Removed from comparison', 'success');
        this.updateComparisonButtons();
    }

    /**
     * Clear all comparisons
     */
    clearComparisons() {
        this.comparisons = [];
        this.saveToStorage();
        this.showToast('Comparison cleared', 'info');
        this.updateComparisonButtons();
    }

    /**
     * Check if product is in comparison
     */
    isInComparison(itemType, itemId) {
        return this.comparisons.some(c => c.itemType === itemType && c.itemId === itemId);
    }

    /**
     * Render floating comparison widget
     */
    renderComparisonWidget() {
        let widget = document.getElementById('productComparisonWidget');
        
        if (!widget) {
            widget = document.createElement('div');
            widget.id = 'productComparisonWidget';
            document.body.appendChild(widget);
        }

        const count = this.comparisons.length;
        const isEmpty = count === 0;

        widget.innerHTML = `
            <div class="comparison-widget ${isEmpty ? 'hidden' : 'visible'} ${count > 0 ? 'with-items' : ''}">
                <div class="comparison-widget-content">
                    <div class="comparison-header">
                        <div class="header-left">
                            <i class="bi bi-columns-gap"></i>
                            <h3>Comparison</h3>
                        </div>
                        <span class="comparison-count" title="Products added to comparison">${count}/${this.maxComparisons}</span>
                    </div>
                    <div class="comparison-list">
                        ${count === 0 ? `
                            <div class="empty-state">
                                <i class="bi bi-inbox"></i>
                                <p>No products selected</p>
                                <small>Click "Compare" on products to add them</small>
                            </div>
                        ` : this.comparisons.map((item, idx) => `
                            <div class="comparison-item" data-index="${idx}">
                                <div class="item-info">
                                    <span class="item-number">${idx + 1}</span>
                                    <span class="item-label">${item.itemType} #${item.itemId}</span>
                                </div>
                                <button class="remove-btn" onclick="productComparison.removeProduct('${item.itemType}', ${item.itemId})" title="Remove from comparison" aria-label="Remove product ${idx + 1}">
                                    <i class="bi bi-x-circle"></i>
                                </button>
                            </div>
                        `).join('')}
                    </div>
                    <div class="comparison-actions">
                        ${count >= 2 ? `
                            <button class="btn-compare-open" onclick="productComparison.openComparison()" title="View side-by-side comparison">
                                <i class="bi bi-eye"></i>
                                <span>View Comparison</span>
                                <span class="badge-count">${count}</span>
                            </button>
                        ` : count > 0 ? `
                            <p class="add-more-msg">
                                <i class="bi bi-info-circle"></i>
                                Add ${this.maxComparisons - count} more to compare
                            </p>
                        ` : ''}
                        ${count > 0 ? `
                            <button class="btn-compare-clear" onclick="productComparison.clearComparisons()" title="Clear all products">
                                <i class="bi bi-trash"></i>
                                <span>Clear All</span>
                            </button>
                        ` : ''}
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Update comparison buttons on product cards
     */
    updateComparisonButtons() {
        const buttons = document.querySelectorAll('.compare-btn');
        buttons.forEach(btn => {
            const itemType = btn.dataset.itemType;
            const itemId = btn.dataset.itemId;
            const isAdded = this.isInComparison(itemType, itemId);
            
            btn.classList.toggle('added', isAdded);
            btn.innerHTML = isAdded 
                ? '<i class="bi bi-check-lg"></i> In Comparison'
                : '<i class="bi bi-columns-gap"></i> Compare';
        });
    }

    /**
     * Open comparison modal
     */
    async openComparison() {
        if (this.comparisons.length < 2) {
            this.showToast('Add at least 2 products to compare', 'warning');
            return;
        }

        const modal = document.getElementById('comparisonModal') || this.createComparisonModal();
        const content = modal.querySelector('.comparison-modal-content');
        
        // Show loading state
        content.innerHTML = '<div class="comparison-loading"><div class="spinner"></div><p>Loading products...</p></div>';
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';

        try {
            const products = await this.fetchProductsForComparison();
            this.renderComparisonTable(content, products);
        } catch (error) {
            console.error('Error loading products:', error);
            content.innerHTML = '<p class="error-msg">Failed to load products for comparison</p>';
        }
    }

    /**
     * Fetch products data from API
     */
    async fetchProductsForComparison() {
        const promises = this.comparisons.map(item =>
            fetch(`/api/quick-view/${item.itemType}/${item.itemId}/`).then(r => r.json())
        );
        return Promise.all(promises);
    }

    /**
     * Render comparison table
     */
    renderComparisonTable(container, products) {
        if (!products || products.length === 0) {
            container.innerHTML = '<p class="error-msg">No products to display</p>';
            return;
        }

        const html = `
            <div class="comparison-table-wrapper">
                <table class="comparison-table">
                    <thead>
                        <tr>
                            <th class="property-col">Property</th>
                            ${products.map((p, idx) => `
                                <th class="product-col product-col-${idx}">
                                    <div class="product-header">
                                        <img src="${p.image}" alt="${p.name}" loading="lazy">
                                        <h4>${p.name}</h4>
                                        <p class="product-rating">★ ${p.rating || 'N/A'}</p>
                                    </div>
                                </th>
                            `).join('')}
                        </tr>
                    </thead>
                    <tbody>
                        ${this.buildComparisonRows(products)}
                    </tbody>
                </table>
            </div>
            <div class="comparison-actions-bottom">
                ${products.map((p, idx) => `
                    <button class="btn-add-to-cart" data-item-type="${p.item_type}" data-item-id="${p.id}">
                        <i class="bi bi-bag-plus"></i> Add to Cart
                    </button>
                `).join('')}
            </div>
        `;

        container.innerHTML = html;
        this.attachComparisonActions(container, products);
    }

    /**
     * Build comparison table rows
     */
    buildComparisonRows(products) {
        const properties = [
            { key: 'price', label: 'Price', format: 'currency' },
            { key: 'stock_status', label: 'Stock Status', format: 'badge' },
            { key: 'material', label: 'Material' },
            { key: 'features', label: 'Key Features', format: 'list' },
            { key: 'sizes', label: 'Available Sizes' },
            { key: 'rating', label: 'Rating' },
            { key: 'review_count', label: 'Reviews' },
            { key: 'long_description', label: 'Description', format: 'text-short' },
        ];

        return properties.map(prop => `
            <tr class="property-row">
                <td class="property-name">${prop.label}</td>
                ${products.map((p, idx) => `
                    <td class="property-value product-col-${idx}">
                        ${this.formatPropertyValue(p[prop.key], prop.format)}
                    </td>
                `).join('')}
            </tr>
        `).join('');
    }

    /**
     * Format property value for display
     */
    formatPropertyValue(value, format) {
        if (!value) return '<span class="not-available">N/A</span>';

        switch (format) {
            case 'currency':
                return `<span class="price-value">Rs ${value}</span>`;
            case 'badge':
                const badgeClass = value === 'In Stock' ? 'badge-in-stock' : 'badge-out-of-stock';
                return `<span class="badge ${badgeClass}">${value}</span>`;
            case 'list':
                if (typeof value === 'string') {
                    return `<ul class="feature-list">${value.split('\n').map(f => `<li>${f.trim()}</li>`).join('')}</ul>`;
                }
                return value;
            case 'text-short':
                const text = typeof value === 'string' ? value : String(value);
                return `<p class="description-text">${text.substring(0, 100)}${text.length > 100 ? '...' : ''}</p>`;
            default:
                return `<span>${value}</span>`;
        }
    }

    /**
     * Attach event listeners to comparison modal actions
     */
    attachComparisonActions(container, products) {
        container.querySelectorAll('.btn-add-to-cart').forEach((btn, idx) => {
            btn.addEventListener('click', () => {
                const itemType = btn.dataset.itemType;
                const itemId = btn.dataset.itemId;
                this.addToCart(itemType, itemId);
            });
        });
    }

    /**
     * Add product to cart
     */
    addToCart(itemType, itemId) {
        // Trigger existing cart functionality
        const event = new CustomEvent('addToCart', {
            detail: { itemType, itemId }
        });
        document.dispatchEvent(event);
        this.showToast('Added to cart', 'success');
    }

    /**
     * Create comparison modal
     */
    createComparisonModal() {
        const modal = document.createElement('div');
        modal.id = 'comparisonModal';
        modal.className = 'comparison-modal';
        modal.innerHTML = `
            <div class="comparison-modal-backdrop" onclick="productComparison.closeComparison()"></div>
            <div class="comparison-modal-container">
                <button class="modal-close" onclick="productComparison.closeComparison()">
                    <i class="bi bi-x-lg"></i>
                </button>
                <div class="comparison-modal-content"></div>
            </div>
        `;
        document.body.appendChild(modal);
        return modal;
    }

    /**
     * Close comparison modal
     */
    closeComparison() {
        const modal = document.getElementById('comparisonModal');
        if (modal) {
            modal.classList.remove('active');
            document.body.style.overflow = 'auto';
        }
    }

    /**
     * Attach global event listeners
     */
    attachEventListeners() {
        // Compare button clicks
        document.addEventListener('click', (e) => {
            const btn = e.target.closest('.compare-btn');
            if (btn) {
                const itemType = btn.dataset.itemType;
                const itemId = btn.dataset.itemId;
                
                if (this.isInComparison(itemType, itemId)) {
                    this.removeProduct(itemType, itemId);
                } else {
                    this.addProduct(itemType, itemId);
                }
            }
        });

        // Close modal on escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeComparison();
            }
        });
    }

    /**
     * Show toast notification
     */
    showToast(message, type = 'info') {
        const container = document.getElementById('toastContainer');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <i class="bi bi-${this.getToastIcon(type)}"></i>
            <span>${message}</span>
        `;

        container.appendChild(toast);

        setTimeout(() => {
            toast.classList.add('show');
        }, 10);

        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    /**
     * Get toast icon based on type
     */
    getToastIcon(type) {
        switch (type) {
            case 'success': return 'check-circle';
            case 'warning': return 'exclamation-circle';
            case 'error': return 'x-circle';
            default: return 'info-circle';
        }
    }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    window.productComparison = new ProductComparison();
});
