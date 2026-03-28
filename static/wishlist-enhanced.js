
class WishlistManager {
    constructor() {
        this.wishlistItems = new Set();
        this.priceAlerts = new Map();
        this.storageKey = 'wishlist-state';
        this.apiBasePath = '/api/wishlist';
        this.isAuthenticated = this.checkAuthentication();

        this.init();
    }

    checkAuthentication() {

        const authEl = document.querySelector('[data-user-authenticated]');
        return authEl ? authEl.dataset.userAuthenticated === 'true' : false;
    }

    init() {
        this.attachEventListeners();
        this.syncWishlistState();
        this.renderAllHeartButtons();
    }

    attachEventListeners() {

        document.addEventListener('click', (e) => {
            const heartBtn = e.target.closest('.wishlist-heart-btn');
            if (heartBtn) {
                e.preventDefault();
                e.stopPropagation();
                this.handleHeartButtonClick(heartBtn);
            }
        });

        document.addEventListener('change', (e) => {
            if (e.target.matches('[data-price-alert-toggle]')) {
                const itemType = e.target.dataset.itemType;
                const itemId = e.target.dataset.itemId;
                this.togglePriceAlert(itemType, itemId, e.target.checked);
            }
        });

        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-share-wishlist]')) {
                e.preventDefault();
                this.openShareWishlistModal();
            }
        });

        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-copy-share-link]')) {
                e.preventDefault();
                this.copyShareLinkToClipboard(e.target);
            }
        });
    }

    handleHeartButtonClick(button) {
        if (!this.isAuthenticated) {
            this.showAuthenticationPrompt();
            return;
        }

        const itemType = button.dataset.itemType;
        const itemId = button.dataset.itemId;
        const isInWishlist = button.classList.contains('in-wishlist');

        if (isInWishlist) {
            this.removeFromWishlist(itemType, itemId, button);
        } else {
            this.addToWishlist(itemType, itemId, button);
        }
    }

    addToWishlist(itemType, itemId, button) {
        const key = `${itemType}-${itemId}`;
        const url = `${this.apiBasePath}/add/`;

        const data = {
            item_type: itemType,
            item_id: itemId,
        };

        const csrfToken = this.getCSRFToken();

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.wishlistItems.add(key);
                if (button) {
                    button.classList.add('in-wishlist');
                    button.setAttribute('aria-pressed', 'true');
                }
                this.showToast('Added to wishlist ❤️', 'success');
                this.updateAllHeartButtons(itemType, itemId, true);
            } else {
                this.showToast(data.error || 'Failed to add to wishlist', 'error');
            }
        })
        .catch(error => {
            console.error('Error adding to wishlist:', error);
            this.showToast('Error adding to wishlist', 'error');
        });
    }

    removeFromWishlist(itemType, itemId, button) {
        const key = `${itemType}-${itemId}`;
        const url = `${this.apiBasePath}/remove/`;

        const data = {
            item_type: itemType,
            item_id: itemId,
        };

        const csrfToken = this.getCSRFToken();

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.wishlistItems.delete(key);
                if (button) {
                    button.classList.remove('in-wishlist');
                    button.setAttribute('aria-pressed', 'false');
                }
                this.showToast('Removed from wishlist', 'info');
                this.updateAllHeartButtons(itemType, itemId, false);
            } else {
                this.showToast(data.error || 'Failed to remove from wishlist', 'error');
            }
        })
        .catch(error => {
            console.error('Error removing from wishlist:', error);
            this.showToast('Error removing from wishlist', 'error');
        });
    }

    togglePriceAlert(itemType, itemId, enabled) {
        const url = `${this.apiBasePath}/toggle-alert/`;
        const csrfToken = this.getCSRFToken();

        const data = {
            item_type: itemType,
            item_id: itemId,
            enabled: enabled,
        };

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.priceAlerts.set(`${itemType}-${itemId}`, enabled);
                const message = enabled ? 'Price alert enabled ✅' : 'Price alert disabled';
                this.showToast(message, 'success');
            } else {
                this.showToast(data.error || 'Failed to update price alert', 'error');
            }
        })
        .catch(error => {
            console.error('Error toggling price alert:', error);
            this.showToast('Error updating price alert', 'error');
        });
    }

    openShareWishlistModal() {
        const modal = document.getElementById('share-wishlist-modal');
        if (!modal) {
            this.createShareWishlistModal();
        } else {
            modal.style.display = 'flex';
            modal.classList.add('active');
        }

        this.generateShareLink();
    }

    createShareWishlistModal() {
        const modal = document.createElement('div');
        modal.id = 'share-wishlist-modal';
        modal.className = 'wishlist-share-modal';
        modal.innerHTML = `
            <div class="wishlist-share-modal-backdrop"></div>
            <div class="wishlist-share-modal-content">
                <button class="wishlist-modal-close" aria-label="Close"><i class="bi bi-x"></i></button>

                <h2>Share Your Wishlist</h2>
                <p>Share your wishlist with friends and family</p>

                <!-- Share Link Section -->
                <div class="wishlist-share-section">
                    <h3>Share Link</h3>
                    <div class="wishlist-share-input-group">
                        <input type="text"
                               id="wishlist-share-url"
                               class="wishlist-share-input"
                               readonly
                               placeholder="Generating share link...">
                        <button class="btn btn-primary" data-copy-share-link>
                            <i class="bi bi-clipboard"></i> Copy Link
                        </button>
                    </div>
                    <small class="wishlist-share-hint">Anyone with this link can view your wishlist</small>
                </div>

                <!-- Social Share Buttons -->
                <div class="wishlist-share-section">
                    <h3>Share on Social Media</h3>
                    <div class="wishlist-social-buttons">
                        <button class="wishlist-social-btn wishlist-social-facebook" data-social="facebook">
                            <i class="bi bi-facebook"></i> Facebook
                        </button>
                        <button class="wishlist-social-btn wishlist-social-twitter" data-social="twitter">
                            <i class="bi bi-twitter"></i> Twitter
                        </button>
                        <button class="wishlist-social-btn wishlist-social-whatsapp" data-social="whatsapp">
                            <i class="bi bi-whatsapp"></i> WhatsApp
                        </button>
                        <button class="wishlist-social-btn wishlist-social-email" data-social="email">
                            <i class="bi bi-envelope"></i> Email
                        </button>
                    </div>
                </div>

                <!-- Share Settings -->
                <div class="wishlist-share-section">
                    <h3>Share Settings</h3>
                    <div class="wishlist-share-options">
                        <label class="wishlist-checkbox-option">
                            <input type="checkbox" data-share-setting="show_prices" checked>
                            <span>Show prices</span>
                        </label>
                        <label class="wishlist-checkbox-option">
                            <input type="checkbox" data-share-setting="show_dates" checked>
                            <span>Show when items were added</span>
                        </label>
                        <label class="wishlist-checkbox-option">
                            <input type="checkbox" data-share-setting="allow_suggestions">
                            <span>Allow others to suggest items</span>
                        </label>
                    </div>
                </div>

                <!-- Expiration Setting -->
                <div class="wishlist-share-section">
                    <h3>Link Expiration</h3>
                    <select id="wishlist-link-expiration" class="wishlist-select">
                        <option value="never">Never expires</option>
                        <option value="7days">Expires in 7 days</option>
                        <option value="30days">Expires in 30 days</option>
                        <option value="90days">Expires in 90 days</option>
                    </select>
                </div>

                <div class="wishlist-share-actions">
                    <button class="btn btn-secondary" id="wishlist-modal-close">Close</button>
                    <button class="btn btn-primary" data-save-share-settings>Save Settings</button>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        modal.querySelector('.wishlist-modal-close').addEventListener('click', () => {
            modal.classList.remove('active');
            modal.style.display = 'none';
        });

        modal.querySelector('#wishlist-modal-close').addEventListener('click', () => {
            modal.classList.remove('active');
            modal.style.display = 'none';
        });

        modal.querySelector('.wishlist-share-modal-backdrop').addEventListener('click', () => {
            modal.classList.remove('active');
            modal.style.display = 'none';
        });

        modal.querySelectorAll('[data-social]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const social = e.currentTarget.dataset.social;
                this.shareOnSocial(social);
            });
        });

        modal.style.display = 'flex';
        modal.classList.add('active');
    }

    generateShareLink() {
        const csrfToken = this.getCSRFToken();
        const url = `${this.apiBasePath}/generate-share-link/`;

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success && data.share_url) {
                const input = document.getElementById('wishlist-share-url');
                if (input) {
                    input.value = data.share_url;
                }
            }
        })
        .catch(error => console.error('Error generating share link:', error));
    }

    copyShareLinkToClipboard(button) {
        const input = document.getElementById('wishlist-share-url');
        if (!input || !input.value) {
            this.showToast('No share link available', 'error');
            return;
        }

        input.select();
        document.execCommand('copy');

        const originalText = button.innerHTML;
        button.innerHTML = '<i class="bi bi-check"></i> Copied!';
        button.classList.add('copied');

        setTimeout(() => {
            button.innerHTML = originalText;
            button.classList.remove('copied');
        }, 2000);

        this.showToast('Link copied to clipboard! 📋', 'success');
    }

    shareOnSocial(platform) {
        const shareUrl = document.getElementById('wishlist-share-url').value;
        if (!shareUrl) {
            this.showToast('Share link not available', 'error');
            return;
        }

        const text = encodeURIComponent('Check out my wishlist!');
        let url;

        switch(platform) {
            case 'facebook':
                url = `https:
                break;
            case 'twitter':
                url = `https:
                break;
            case 'whatsapp':
                url = `https:
                break;
            case 'email':
                url = `mailto:?subject=Check out my wishlist&body=${text}%20${encodeURIComponent(shareUrl)}`;
                break;
        }

        if (url) {
            window.open(url, '_blank', 'width=600,height=400');
        }
    }

    syncWishlistState() {
        const csrfToken = this.getCSRFToken();
        const url = `${this.apiBasePath}/sync-state/`;

        fetch(url, {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrfToken,
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.items) {
                this.wishlistItems.clear();
                data.items.forEach(item => {
                    const key = `${item.item_type}-${item.item_id}`;
                    this.wishlistItems.add(key);
                    if (item.price_alert_enabled) {
                        this.priceAlerts.set(key, true);
                    }
                });
                this.renderAllHeartButtons();
            }
        })
        .catch(error => console.error('Error syncing wishlist state:', error));
    }

    renderAllHeartButtons() {
        document.querySelectorAll('.wishlist-heart-btn').forEach(btn => {
            const itemType = btn.dataset.itemType;
            const itemId = btn.dataset.itemId;
            const key = `${itemType}-${itemId}`;

            if (this.wishlistItems.has(key)) {
                btn.classList.add('in-wishlist');
                btn.setAttribute('aria-pressed', 'true');
            } else {
                btn.classList.remove('in-wishlist');
                btn.setAttribute('aria-pressed', 'false');
            }
        });
    }

    updateAllHeartButtons(itemType, itemId, inWishlist) {
        document.querySelectorAll(`[data-item-type="${itemType}"][data-item-id="${itemId}"]`).forEach(btn => {
            if (inWishlist) {
                btn.classList.add('in-wishlist');
                btn.setAttribute('aria-pressed', 'true');
            } else {
                btn.classList.remove('in-wishlist');
                btn.setAttribute('aria-pressed', 'false');
            }
        });
    }

    showAuthenticationPrompt() {
        this.showToast('Please log in to use wishlist', 'warning');

        setTimeout(() => {
            window.location.href = '/login/';
        }, 1500);
    }

    showToast(message, type = 'info') {
        const container = document.getElementById('toastContainer') || this.createToastContainer();

        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.role = 'alert';
        toast.innerHTML = `
            <div class="toast-content">
                <i class="bi bi-${this.getToastIcon(type)}"></i>
                <span>${message}</span>
            </div>
            <button class="toast-close" aria-label="Close">
                <i class="bi bi-x"></i>
            </button>
        `;

        container.appendChild(toast);

        const timeout = setTimeout(() => {
            toast.classList.add('removing');
            setTimeout(() => toast.remove(), 300);
        }, 3000);

        toast.querySelector('.toast-close').addEventListener('click', () => {
            clearTimeout(timeout);
            toast.classList.add('removing');
            setTimeout(() => toast.remove(), 300);
        });
    }

    createToastContainer() {
        const container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container';
        document.body.appendChild(container);
        return container;
    }

    getToastIcon(type) {
        const icons = {
            success: 'check-circle-fill',
            error: 'exclamation-circle-fill',
            warning: 'exclamation-triangle-fill',
            info: 'info-circle-fill',
        };
        return icons[type] || icons.info;
    }

    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
               document.querySelector('meta[name="csrf-token"]')?.content || '';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.wishlistManager = new WishlistManager();
});
