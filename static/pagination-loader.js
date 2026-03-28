
class PaginationLoader {
    constructor(options = {}) {
        this.categoryType = options.categoryType || null;
        this.currentPage = 1;
        this.totalPages = 1;
        this.isLoading = false;
        this.isMobile = window.innerWidth <= 768;
        this.enableInfiniteScroll = options.enableInfiniteScroll !== false && this.isMobile;
        this.infiniteScrollThreshold = options.infiniteScrollThreshold || 300;
        this.productsPerPage = options.productsPerPage || 12;

        this.productContainer = options.productContainer || '.grid, .arrivals-list, .toys-grid';
        this.paginationContainer = options.paginationContainer || '.pagination-nav, .load-more-section';
        this.loadMoreButton = options.loadMoreButton || '.load-more-btn';
        this.infiniteScrollIndicator = options.infiniteScrollIndicator || '.infinite-scroll-indicator';

        this.filters = {
            q: new URLSearchParams(window.location.search).get('q') || '',
            subcategory: new URLSearchParams(window.location.search).get('subcategory') || 'all',
            sort: new URLSearchParams(window.location.search).get('sort') || 'featured',
            min_price: new URLSearchParams(window.location.search).get('min_price') || '',
            max_price: new URLSearchParams(window.location.search).get('max_price') || '',
        };

        this.onBeforeLoad = options.onBeforeLoad || null;
        this.onAfterLoad = options.onAfterLoad || null;
        this.onError = options.onError || null;

        this.init();
    }

    init() {

        const pageInfo = document.querySelector('[data-total-pages]');
        if (pageInfo) {
            this.totalPages = parseInt(pageInfo.dataset.totalPages);
        }

        this.setupLoadMoreButton();

        if (this.enableInfiniteScroll) {
            this.setupInfiniteScroll();
        }

        window.addEventListener('resize', () => this.handleResize());
    }

    setupLoadMoreButton() {
        const buttons = document.querySelectorAll('.load-more-btn');
        buttons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                this.loadNextPage();
            });
        });
    }

    setupInfiniteScroll() {
        window.addEventListener('scroll', () => this.handleScroll());

        const sentinel = document.querySelector('.infinite-scroll-sentinel');
        if (sentinel && 'IntersectionObserver' in window) {
            const observer = new IntersectionObserver(
                (entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting && !this.isLoading && this.currentPage < this.totalPages) {
                            this.loadNextPage();
                        }
                    });
                },
                { rootMargin: '300px' }
            );
            observer.observe(sentinel);
        }
    }

    handleScroll() {
        if (this.isLoading || this.currentPage >= this.totalPages) return;

        const scrollPosition = window.innerHeight + window.scrollY;
        const pageHeight = document.documentElement.scrollHeight;

        if (pageHeight - scrollPosition < this.infiniteScrollThreshold) {
            this.loadNextPage();
        }
    }

    handleResize() {
        const wasMobile = this.isMobile;
        this.isMobile = window.innerWidth <= 768;

        if (this.isMobile && !wasMobile && this.enableInfiniteScroll) {
            this.setupInfiniteScroll();
        }
    }

    async loadNextPage() {
        if (this.isLoading || this.currentPage >= this.totalPages) return;

        this.currentPage++;
        await this.loadProducts();
    }

    async loadProducts() {
        this.isLoading = true;

        const button = document.querySelector('.load-more-btn');
        if (button) {
            button.disabled = true;
            button.innerHTML = '<span class="loading-spinner"></span> Loading...';
        }

        this.showLoadingIndicator();

        if (this.onBeforeLoad) this.onBeforeLoad();

        try {
            const response = await fetch(
                `/api/load-products/${this.categoryType}/?page=${this.currentPage}&` +
                `q=${encodeURIComponent(this.filters.q)}&` +
                `subcategory=${this.filters.subcategory}&` +
                `sort=${this.filters.sort}&` +
                `min_price=${this.filters.min_price}&` +
                `max_price=${this.filters.max_price}&` +
                `per_page=${this.productsPerPage}`
            );

            if (!response.ok) throw new Error(`HTTP ${response.status}`);

            const data = await response.json();

            if (!data.success) throw new Error(data.error || 'Failed to load products');

            this.renderProducts(data.products);

            this.totalPages = data.total_pages;
            this.currentPage = data.page;

            this.updateLoadMoreButton(data.has_next);

            if (this.onAfterLoad) this.onAfterLoad(data);

            if (window.updateCartUI) window.updateCartUI();
            if (window.WishlistManager) window.WishlistManager.syncWishlistState();

        } catch (error) {
            console.error('Error loading products:', error);
            this.showError('Failed to load more products. Please try again.');

            if (this.onError) this.onError(error);

            this.currentPage--;

        } finally {
            this.isLoading = false;

            const button = document.querySelector('.load-more-btn');
            if (button) {
                button.disabled = false;
                button.innerHTML = '↓ Load More Products';
            }

            this.hideLoadingIndicator();
        }
    }

    renderProducts(products) {
        const containers = document.querySelectorAll('.grid, .arrivals-list, .toys-grid');
        if (containers.length === 0) return;

        const container = containers[0];

        const productHTMLs = products.map(product => {

            const existingProduct = container.querySelector('article, .arrival-card, .toy-card');

            if (existingProduct && existingProduct.classList.contains('arrival-card')) {
                return this.createArrivalCardHTML(product);
            } else if (existingProduct && existingProduct.classList.contains('toy-card')) {
                return this.createToyCardHTML(product);
            } else {
                return this.createProductCardHTML(product);
            }
        });

        const tempDiv = document.createElement('div');
        productHTMLs.forEach(html => {
            tempDiv.innerHTML = html;
            while (tempDiv.firstChild) {
                container.appendChild(tempDiv.firstChild);
            }
        });

        this.reinitializeElements();
    }

    createProductCardHTML(product) {
        const rating = product.reviews > 0
            ? `<div class="rating"><span>${product.rating.toFixed(1)}★</span> (${product.reviews})</div>`
            : '';

        return `
            <article class="men-card men-product" data-name="${product.name.toLowerCase()}" data-price="${product.price}">
                <div class="aspect-[4/5] bg-sky-50 overflow-hidden relative group">
                    <img src="${product.image}" alt="${product.name}" class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-110" loading="lazy">
                    <button class="quick-view-btn absolute inset-0 bg-black/50 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300" data-item-type="${product.type}" data-item-id="${product.id}" style="border: none; width: 100%; height: 100%; cursor: pointer;">
                        <span class="bg-white text-slate-900 px-5 py-2.5 rounded-lg font-bold text-sm hover:scale-105 transition-transform"><i class="bi bi-eye"></i> Quick View</span>
                    </button>
                    <div class="absolute top-3 right-3 z-10">
                        <button class="wishlist-heart-btn" data-item-type="${product.type}" data-item-id="${product.id}" aria-label="Add to wishlist" aria-pressed="false" title="Add to Wishlist">
                            <i class="bi bi-heart"></i>
                        </button>
                    </div>
                </div>
                <div class="p-4 grid gap-2">
                    <h3 class="font-extrabold text-slate-900 leading-6"><a href="${product.url}" class="hover:text-blue-600 transition-colors" style="color:inherit;text-decoration:none">${product.name}</a></h3>
                    ${rating}
                    <div class="flex items-center gap-2 flex-wrap">
                        <span class="text-lg font-extrabold text-slate-900">Rs ${product.price}</span>
                    </div>
                    <div class="grid grid-cols-[1fr_auto_auto] gap-2 pt-1">
                        <a href="${product.url}" class="rounded-lg border border-indigo-200 bg-indigo-50 py-2 text-center text-sm font-bold text-indigo-700"><i class="bi bi-eye"></i> View</a>
                        <button class="rounded-lg bg-gradient-to-r from-blue-600 to-teal-600 px-3 py-2 text-sm font-bold text-white" data-add-to-cart data-item-type="${product.type}" data-item-id="${product.id}"><i class="bi bi-bag-plus"></i></button>
                        <button class="compare-btn" data-item-type="${product.type}" data-item-id="${product.id}" type="button" title="Add to comparison - Compare up to 4 products side by side" aria-label="Add to comparison"><i class="bi bi-columns-gap"></i><span class="btn-text">Compare</span><span class="btn-feedback"></span></button>
                    </div>
                </div>
            </article>
        `;
    }

    createArrivalCardHTML(product) {
        const rating = product.reviews > 0
            ? `<div style="text-align:center;font-size:12px;margin:8px 0;"><span>${product.rating.toFixed(1)}★</span> (${product.reviews})</div>`
            : '';

        return `
            <article class="arrival-card">
                <div class="arrival-media">
                    <img src="${product.image}" alt="${product.name}" loading="lazy">
                    <button class="quick-view-btn arrival-overlay" data-item-type="${product.type}" data-item-id="${product.id}" style="background: none; border: none; color: inherit; cursor: pointer; padding: 0; text-decoration: none; display: flex; align-items: center; justify-content: center; width: 100%; height: 100%;"><span><i class="bi bi-eye"></i> Quick View</span></button>
                    <div style="position: absolute; top: 12px; right: 12px; z-index: 10;">
                        <button class="wishlist-heart-btn" data-item-type="${product.type}" data-item-id="${product.id}" aria-label="Add to wishlist" aria-pressed="false" title="Add to Wishlist">
                            <i class="bi bi-heart"></i>
                        </button>
                    </div>
                </div>
                <h3><a href="${product.url}" style="color:inherit;text-decoration:none">${product.name}</a></h3>
                <p style="font-size:13px;color:#666;margin:8px 0;">New arrival</p>
                ${rating}
                <div class="arrival-meta">
                    <span class="price">Rs ${product.price}</span>
                    <div style="display: flex; gap: 8px;">
                        <a href="javascript:void(0)" class="arrival-btn" data-add-to-cart data-item-type="${product.type}" data-item-id="${product.id}"><i class="bi bi-bag-plus"></i> Add to cart</a>
                        <button class="compare-btn" data-item-type="${product.type}" data-item-id="${product.id}" type="button" title="Add to comparison - Compare up to 4 products side by side" aria-label="Add to comparison" style="padding: 6px 10px; border-radius: 6px;"><i class="bi bi-columns-gap"></i></button>
                    </div>
                </div>
            </article>
        `;
    }

    createToyCardHTML(product) {
        const rating = product.reviews > 0
            ? `<div class="toy-rating" style="text-align:center;font-size:12px;margin:8px 0;"><span>${product.rating.toFixed(1)}★</span> (${product.reviews})</div>`
            : '';

        return `
            <div class="toy-card">
                <div class="toy-image">
                    <img src="${product.image}" alt="${product.name}" loading="lazy">
                    <div class="toy-overlay">
                        <button class="quick-view-btn" data-item-type="toy" data-item-id="${product.id}" style="background: none; border: none; color: inherit; cursor: pointer; font-size: inherit; padding: 0;"><i class="bi bi-eye"></i> Quick View</button>
                        <div style="position: absolute; top: 12px; right: 12px;">
                            <button class="wishlist-heart-btn" data-item-type="toy" data-item-id="${product.id}" aria-label="Add to wishlist" aria-pressed="false" title="Add to Wishlist">
                                <i class="bi bi-heart"></i>
                            </button>
                        </div>
                    </div>
                </div>
                <div class="toy-content">
                    <h3><a href="${product.url}" style="color:inherit;text-decoration:none">${product.name}</a></h3>
                    ${rating}
                    <div class="price-container">
                        <span class="price-current">Rs ${product.price}</span>
                    </div>
                    <div class="toy-actions">
                        <a href="${product.url}" class="toy-link"><i class="bi bi-eye"></i> View</a>
                        <button class="toy-cart" data-add-to-cart data-item-type="toy" data-item-id="${product.id}"><i class="bi bi-bag-plus"></i> Add</button>
                        <button class="compare-btn" data-item-type="toy" data-item-id="${product.id}" type="button" title="Add to comparison - Compare up to 4 products side by side" aria-label="Add to comparison"><i class="bi bi-columns-gap"></i></button>
                    </div>
                </div>
            </div>
        `;
    }

    reinitializeElements() {

        if (window.initializeQuickView) {
            const buttons = document.querySelectorAll('.quick-view-btn');
            buttons.forEach(button => {
                button.removeEventListener('click', window.handleQuickViewClick);
                button.addEventListener('click', window.handleQuickViewClick);
            });
        }

        if (window.initializeCartButtons) {
            const cartButtons = document.querySelectorAll('[data-add-to-cart]');
            cartButtons.forEach(button => {
                button.removeEventListener('click', window.handleAddToCart);
                button.addEventListener('click', window.handleAddToCart);
            });
        }

        if (window.WishlistManager) {
            window.WishlistManager.renderAllHeartButtons();
        }

        if (window.updateCartUI) {
            window.updateCartUI();
        }
    }

    updateLoadMoreButton(hasMore) {
        const button = document.querySelector('.load-more-btn');
        if (!button) return;

        if (hasMore) {
            button.style.display = 'block';
            button.disabled = false;
        } else {
            button.style.display = 'none';

            const endMessage = document.querySelector('.load-more-end');
            if (endMessage) {
                endMessage.style.display = 'block';
            }
        }
    }

    showLoadingIndicator() {
        const indicator = document.querySelector('.infinite-scroll-indicator');
        if (indicator) {
            indicator.style.display = 'flex';
        }
    }

    hideLoadingIndicator() {
        const indicator = document.querySelector('.infinite-scroll-indicator');
        if (indicator) {
            indicator.style.display = 'none';
        }
    }

    showError(message) {

        if (window.showToast) {
            window.showToast(message, 'error');
        } else {
            alert(message);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {

    const categoryType = document.body.dataset.categoryType ||
                        new URLSearchParams(window.location.pathname).get('category') ||
                        (window.location.pathname.includes('mens') && 'men') ||
                        (window.location.pathname.includes('women') && 'women') ||
                        (window.location.pathname.includes('kids') && 'kids') ||
                        (window.location.pathname.includes('toys') && 'toys');

    if (categoryType) {
        window.paginationLoader = new PaginationLoader({
            categoryType: categoryType,
            enableInfiniteScroll: true,
        });
    }
});
