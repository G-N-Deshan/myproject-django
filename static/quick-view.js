/**
 * QUICK-VIEW MODAL FUNCTIONALITY
 * Opens product details in a modal without page navigation
 */

class QuickViewModal {
    constructor() {
        this.modal = null;
        this.backdrop = null;
        this.currentProduct = null;
        this.init();
    }

    init() {
        // Create modal if it doesn't exist
        if (!document.getElementById('quickViewModal')) {
            this.createModal();
        }
        this.attachEventListeners();
    }

    createModal() {
        const html = `
            <div class="quick-view-backdrop" id="quickViewBackdrop"></div>
            <div class="quick-view-modal" id="quickViewModal">
                <button class="quick-view-close" aria-label="Close">&times;</button>
                <div class="quick-view-content" id="quickViewContent">
                    <div class="qv-loading"></div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', html);
        this.modal = document.getElementById('quickViewModal');
        this.backdrop = document.getElementById('quickViewBackdrop');
    }

    attachEventListeners() {
        // Close button
        document.addEventListener('click', (e) => {
            if (e.target.closest('.quick-view-close')) {
                this.close();
            }
            if (e.target.id === 'quickViewBackdrop') {
                this.close();
            }
        });

        // Quick view buttons on products
        document.addEventListener('click', (e) => {
            const btn = e.target.closest('.quick-view-btn');
            if (btn) {
                const itemType = btn.dataset.itemType;
                const itemId = btn.dataset.itemId;
                this.open(itemType, itemId);
            }
        });

        // Keyboard: Escape to close
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.close();
            }
        });

        // Size/option selection
        document.addEventListener('click', (e) => {
            const optBtn = e.target.closest('.qv-option-btn');
            if (optBtn && this.modal?.classList.contains('active')) {
                optBtn.parentElement.querySelectorAll('.qv-option-btn').forEach(btn => {
                    btn.classList.remove('selected');
                });
                optBtn.classList.add('selected');
            }
        });

        // Thumbnail clicks to change main image
        document.addEventListener('click', (e) => {
            const thumb = e.target.closest('.qv-thumbnail');
            if (thumb && this.modal?.classList.contains('active')) {
                const mainImg = document.querySelector('.qv-main-image');
                if (mainImg) {
                    mainImg.src = thumb.querySelector('img').src;
                    mainImg.alt = thumb.querySelector('img').alt;
                }
                // Update active thumbnail
                document.querySelectorAll('.qv-thumbnail').forEach(t => {
                    t.classList.remove('active');
                });
                thumb.classList.add('active');
            }
        });
    }

    async open(itemType, itemId) {
        this.modal.classList.add('active');
        this.backdrop.classList.add('active');
        document.body.style.overflow = 'hidden';

        // Load product data
        await this.loadProduct(itemType, itemId);
    }

    close() {
        this.modal.classList.remove('active');
        this.backdrop.classList.remove('active');
        document.body.style.overflow = 'auto';
    }

    async loadProduct(itemType, itemId) {
        const content = document.getElementById('quickViewContent');
        content.innerHTML = '<div class="qv-loading"></div>';

        try {
            const response = await fetch(`/api/quick-view/${itemType}/${itemId}/`);
            if (!response.ok) throw new Error('Failed to load product');

            const product = await response.json();
            content.innerHTML = this.buildProductHTML(product, itemType);
            this.currentProduct = { ...product, itemType, itemId };
        } catch (error) {
            console.error('Error loading product:', error);
            content.innerHTML = `
                <div style="padding: 40px; text-align: center;">
                    <p style="color: #ef4444; font-weight: 600;">Failed to load product details</p>
                </div>
            `;
        }
    }

    buildProductHTML(product, itemType) {
        const discountPercent = product.discount_percentage || 0;
        const stockStatus = this.getStockStatus(product);
        const rating = product.rating || 0;
        const ratingCount = product.rating_count || 0;

        return `
            <div class="qv-image-section">
                <img src="${product.image}" alt="${product.name}" class="qv-main-image">
                ${product.images && product.images.length > 1 ? `
                    <div class="qv-thumbnails">
                        ${product.images.map((img, i) => `
                            <div class="qv-thumbnail ${i === 0 ? 'active' : ''}">
                                <img src="${img}" alt="Product image ${i + 1}">
                            </div>
                        `).join('')}
                    </div>
                ` : ''}
            </div>

            <div class="qv-details">
                ${product.badge ? `<div class="qv-badge">${product.badge}</div>` : ''}
                
                <h2 class="qv-title">${product.name}</h2>

                ${rating > 0 ? `
                    <div class="qv-rating">
                        <span class="qv-stars">${'★'.repeat(Math.round(rating))}${'☆'.repeat(5 - Math.round(rating))}</span>
                        <span>${rating}/5 ${ratingCount > 0 ? `(${ratingCount} reviews)` : ''}</span>
                    </div>
                ` : ''}

                <div class="qv-price">
                    <span class="qv-current-price">$${parseFloat(product.price).toFixed(2)}</span>
                    ${product.original_price && product.original_price > product.price ? `
                        <span class="qv-original-price">$${parseFloat(product.original_price).toFixed(2)}</span>
                        <span class="qv-discount">${discountPercent}% OFF</span>
                    ` : ''}
                </div>

                <div class="qv-stock ${stockStatus.class}">
                    ${stockStatus.text}
                </div>

                <p class="qv-description">${product.description || ''}</p>

                <div class="qv-divider"></div>

                ${product.sizes && product.sizes.length > 0 ? `
                    <div class="qv-options">
                        <label class="qv-option-label">Size</label>
                        <div class="qv-option-values">
                            ${product.sizes.map(size => `
                                <button class="qv-option-btn ${product.sizes[0] === size ? 'selected' : ''}" data-size="${size}">
                                    ${size}
                                </button>
                            `).join('')}
                        </div>
                    </div>
                ` : ''}

                ${product.colors && product.colors.length > 0 ? `
                    <div class="qv-options">
                        <label class="qv-option-label">Color</label>
                        <div class="qv-option-values">
                            ${product.colors.map(color => `
                                <button class="qv-option-btn" data-color="${color}" style="border-left: 4px solid ${color};">
                                    ${color}
                                </button>
                            `).join('')}
                        </div>
                    </div>
                ` : ''}

                <div class="qv-actions">
                    <button class="qv-add-to-cart" data-item-type="${itemType}" data-item-id="${product.id}">
                        <i class="bi bi-bag-plus"></i> Add to Cart
                    </button>
                    <button class="qv-wishlist-btn" data-item-type="${itemType}" data-item-id="${product.id}" ${product.is_wishlisted ? 'class="qv-wishlist-btn wishlisted"' : ''}>
                        <i class="bi ${product.is_wishlisted ? 'bi-heart-fill' : 'bi-heart'}"></i>
                    </button>
                </div>

                <a href="${product.detail_url}" class="qv-view-details">
                    View Full Details
                </a>
            </div>
        `;
    }

    getStockStatus(product) {
        const stock = product.stock_level || 0;
        
        if (stock <= 0) {
            return {
                text: '❌ Out of Stock',
                class: 'out-of-stock'
            };
        } else if (stock <= 5) {
            return {
                text: `⚠️ Only ${stock} left!`,
                class: 'low-stock'
            };
        } else {
            return {
                text: '✓ In Stock',
                class: 'in-stock'
            };
        }
    }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    window.quickViewModal = new QuickViewModal();

    // Handle "Add to Cart" from quick view
    document.addEventListener('click', (e) => {
        const btn = e.target.closest('.qv-add-to-cart');
        if (btn) {
            const itemType = btn.dataset.itemType;
            const itemId = btn.dataset.itemId;
            const selectedSize = document.querySelector('.qv-option-btn[data-size].selected')?.dataset.size;
            const selectedColor = document.querySelector('.qv-option-btn[data-color].selected')?.dataset.color;

            // Call existing addToCart function with options
            if (window.addToCart) {
                window.addToCart(itemType, itemId, btn, { size: selectedSize, color: selectedColor });
            }
        }
    });

    // Handle "Add to Wishlist" from quick view
    document.addEventListener('click', (e) => {
        const btn = e.target.closest('.qv-wishlist-btn');
        if (btn) {
            const itemType = btn.dataset.itemType;
            const itemId = btn.dataset.itemId;
            toggleWishlist(itemType, itemId, btn);
        }
    });
});

async function toggleWishlist(itemType, itemId, button) {
    try {
        const response = await fetch('/api/wishlist/toggle/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                item_type: itemType,
                item_id: itemId
            })
        });

        const data = await response.json();
        
        if (data.added) {
            button.classList.add('wishlisted');
            button.innerHTML = '<i class="bi bi-heart-fill"></i> Wishlisted';
            showGlobalToast('Added to wishlist!', 'success');
        } else {
            button.classList.remove('wishlisted');
            button.innerHTML = '<i class="bi bi-heart"></i> Add to Wishlist';
            showGlobalToast('Removed from wishlist', 'success');
        }
    } catch (error) {
        console.error('Error toggling wishlist:', error);
        showGlobalToast('Error updating wishlist', 'error');
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
