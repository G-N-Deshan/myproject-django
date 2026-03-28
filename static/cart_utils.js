
if (!document.getElementById('cartSpinStyle')) {
    const s = document.createElement('style');
    s.id = 'cartSpinStyle';
    s.textContent = `
        @keyframes cartSpin{to{transform:rotate(360deg)}}
        @keyframes slideIn{from{transform:translateX(400px);opacity:0}to{transform:translateX(0);opacity:1}}
        @keyframes slideOut{from{transform:translateX(0);opacity:1}to{transform:translateX(400px);opacity:0}}
    `;
    document.head.appendChild(s);
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

if (window.__cartUtilsBootstrapped) {
    console.log('✓ Cart Utils already loaded, skipping initialization');
} else {
    window.__cartUtilsBootstrapped = true;

    async function addToCart(itemType, itemId, buttonElement = null) {
        const fallbackUrl = `/cart/add/${itemType}/${itemId}/`;

        try {
            if (buttonElement?.dataset.loading === '1') return false;
            if (buttonElement) {
                buttonElement.dataset.loading = '1';
                buttonElement._origHTML = buttonElement.innerHTML;
                buttonElement.innerHTML = '<span class="cart-spinner" style="display:inline-block;width:14px;height:14px;border:2px solid rgba(255,255,255,.4);border-top-color:#fff;border-radius:50%;animation:cartSpin .5s linear infinite;vertical-align:middle;margin-right:6px;"></span> Adding...';
                buttonElement.disabled = true;
            }

            const csrftoken = getCookie('csrftoken');

            if (!csrftoken) {
                window.location.href = fallbackUrl;
                return false;
            }

            const response = await fetch(fallbackUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {

                window.location.href = fallbackUrl;
                return false;
            }

            const data = await response.json();

            if (data.success) {
                updateGlobalCartCount(data.cart_count);

                if (buttonElement) {
                    const origHTML = buttonElement._origHTML || buttonElement.textContent;
                    const originalBg = buttonElement.style.background;
                    buttonElement.innerHTML = '✓ Added!';
                    buttonElement.style.background = '#10b981';

                    setTimeout(() => {
                        buttonElement.innerHTML = origHTML;
                        buttonElement.style.background = originalBg;
                    }, 1200);
                }

                showGlobalToast(data.message);
                return true;
            }

            showGlobalToast('Error: ' + (data.error || 'Failed'), 'error');
            return false;
        } catch (error) {
            console.error('Error adding to cart:', error);

            window.location.href = fallbackUrl;
            return false;
        } finally {
            if (buttonElement) {
                delete buttonElement.dataset.loading;
                buttonElement.disabled = false;
            }
        }
    }

    window.addToCart = addToCart;

    document.addEventListener('DOMContentLoaded', function () {
        console.log('🛒 Cart Utils: Initializing global cart functionality...');
        loadCartCount();

        document.body.addEventListener('click', function (e) {
            const btn = e.target.closest('[data-add-to-cart]');
            if (!btn) return;

            const itemType = btn.dataset.itemType;
            const itemId = btn.dataset.itemId;

            if (!itemType || !itemId) {
                console.error('Missing data-item-type or data-item-id:', btn);
                return;
            }

            e.preventDefault();
            e.stopPropagation();
            console.log(`Adding ${itemType} #${itemId} to cart...`);
            addToCart(itemType, itemId, btn);
        });

        console.log('✅ Cart Utils: Ready!');
    });
}

function updateGlobalCartCount(count) {
    const cartElements = document.querySelectorAll('.cart-count, .cart-badge, [data-cart-count]');
    cartElements.forEach(el => {
        el.textContent = count;
        if (count > 0) {
            el.style.display = 'inline-block';
            el.classList.add('has-items');
        } else {
            el.classList.remove('has-items');
        }
    });

    try {
        localStorage.setItem('kids_cart_count', count);
    } catch(e) {

    }
}

function showGlobalToast(message, type = 'success') {
    const existing = document.querySelector('.global-toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'global-toast';

    const iconSpan = document.createElement('span');
    iconSpan.style.marginRight = '0.5rem';
    iconSpan.style.fontSize = '1.2rem';
    iconSpan.textContent = type === 'success' ? '✓' : '⚠';

    const msgSpan = document.createElement('span');
    msgSpan.textContent = message;

    toast.appendChild(iconSpan);
    toast.appendChild(msgSpan);

    const bgColor = type === 'success' ? 'linear-gradient(135deg, #10b981 0%, #059669 100%)' : 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)';

    toast.style.cssText = `
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        background: ${bgColor};
        color: #fff;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        z-index: 99999;
        animation: slideIn 0.3s ease;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        display: flex;
        align-items: center;
        max-width: 350px;
        word-wrap: break-word;
    `;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

async function loadCartCount() {
    try {
        const response = await fetch('/cart/get/');
        const data = await response.json();

        if (data.success) {
            updateGlobalCartCount(data.cart_count);
        }
    } catch (error) {
        console.error('Error loading cart count:', error);
    }
}

if (!document.querySelector('#cart-utils-styles')) {
    const style = document.createElement('style');
    style.id = 'cart-utils-styles';
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(400px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(400px); opacity: 0; }
        }
        .cart-badge.has-items {
            animation: pulse 0.3s ease;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.2); }
        }
        [data-add-to-cart] {
            cursor: pointer;
            transition: all 0.2s ease;
        }
        [data-add-to-cart]:hover {
            opacity: 0.9;
            transform: translateY(-1px);
        }
    `;
    document.head.appendChild(style);
}

console.log('✅ cart_utils.js loaded');
