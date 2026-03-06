/**
 * WHY: Countdown timer for hot offers
 * Shows remaining time for each offer
 */
function initOfferTimers() {
    const timers = document.querySelectorAll('.offer-timer');
    
    timers.forEach(timer => {
        const countdown = timer.querySelector('.countdown');
        if (!countdown) return;
        
        // Get end time from data attribute
        let endTime;
        if (timer.dataset.endTime) {
            endTime = new Date(timer.dataset.endTime).getTime();
        } else {
            // Default: 24 hours from now
            endTime = new Date().getTime() + (24 * 60 * 60 * 1000);
        }
        
        // Check if end time is valid
        if (isNaN(endTime)) {
            console.error('Invalid end time:', timer.dataset.endTime);
            countdown.textContent = '24h 00m 00s';
            endTime = new Date().getTime() + (24 * 60 * 60 * 1000);
        }
        
        // Update countdown every second
        const interval = setInterval(() => {
            const now = new Date().getTime();
            const distance = endTime - now;
            
            if (distance < 0) {
                countdown.textContent = 'EXPIRED';
                clearInterval(interval);
                timer.style.background = '#fecaca';
                timer.style.borderColor = '#fca5a5';
                return;
            }
            
            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);
            
            // Format with leading zeros
            const formatTime = (num) => String(num).padStart(2, '0');
            
            countdown.textContent = `${formatTime(days)}d ${formatTime(hours)}h ${formatTime(minutes)}m ${formatTime(seconds)}s`;
        }, 1000);
    });
}

/**
 * WHY: Smooth horizontal scrolling for arrivals slider
 * Better UX than default scroll
 */
function initArrivalsSlider() {
    const track = document.querySelector('.arrivals-track');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');
    
    if (!track || !prevBtn || !nextBtn) {
        console.log('Slider elements not found');
        return;
    }
    
    const scrollAmount = 360; // card width + gap
    
    prevBtn.addEventListener('click', () => {
        track.scrollBy({
            left: -scrollAmount,
            behavior: 'smooth'
        });
    });
    
    nextBtn.addEventListener('click', () => {
        track.scrollBy({
            left: scrollAmount,
            behavior: 'smooth'
        });
    });
    
    // Update button states based on scroll position
    function updateButtons() {
        const maxScroll = track.scrollWidth - track.clientWidth;
        
        if (track.scrollLeft <= 0) {
            prevBtn.style.opacity = '0.3';
            prevBtn.style.pointerEvents = 'none';
        } else {
            prevBtn.style.opacity = '1';
            prevBtn.style.pointerEvents = 'auto';
        }
        
        if (track.scrollLeft >= maxScroll - 5) {
            nextBtn.style.opacity = '0.3';
            nextBtn.style.pointerEvents = 'none';
        } else {
            nextBtn.style.opacity = '1';
            nextBtn.style.pointerEvents = 'auto';
        }
    }
    
    track.addEventListener('scroll', updateButtons);
    updateButtons();
}

/**
 * WHY: Wishlist heart button toggle
 * Gives instant feedback when adding to wishlist
 */
function initWishlistButtons() {
    const wishlistBtns = document.querySelectorAll('.wishlist-btn');
    
    wishlistBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            
            btn.classList.toggle('active');
            
            const heart = btn.querySelector('.heart-icon');
            if (btn.classList.contains('active')) {
                heart.textContent = '♥';
                showToast('Added to wishlist ❤️');
            } else {
                heart.textContent = '♡';
                showToast('Removed from wishlist');
            }
        });
    });
}

/**
 * WHY: Simple toast notification
 * Shows user feedback for actions
 */
function showToast(message) {
    const existing = document.querySelector('.toast-notification');
    if (existing) existing.remove();
    
    const toast = document.createElement('div');
    toast.className = 'toast-notification';
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        background: rgba(15, 23, 42, 0.95);
        color: #fff;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        z-index: 9999;
        animation: slideIn 0.3s ease;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 2500);
}

/**
 * WHY: Card click handler for navigation
 * Makes cards clickable to go to specific pages
 */
function setupCardClickHandlers() {
    const cards = document.querySelectorAll('.feature-card');
    
    cards.forEach(card => {
        const cardName = (card.querySelector('h2')?.textContent || '').toLowerCase();

        card.style.cursor = 'pointer';
        card.addEventListener('click', function (e) {
            if (e.target.closest('button, a')) return;

            if (cardName.includes('cloth') || cardName.includes('fashion')) {
                window.location.href = '/cloths/';
            } else if (cardName.includes('toy')) {
                window.location.href = '/toys/';
            } else {
                window.location.href = '/buy/';
            }
        });
    });
}

// Add animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(400px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(400px); opacity: 0; }
    }
`;
document.head.appendChild(style);

/**
 * Initialize all features on page load
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Initializing home page features...');
    initOfferTimers();
    initArrivalsSlider();
    initWishlistButtons();
    setupCardClickHandlers();
    // bindHomeAddToCart(); // handled globally by cart_utils.js
    console.log('✅ All home page features initialized!');
});

// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }

// function updateCartCountInUI(count) {
//     document.querySelectorAll('.cart-count, .cart-badge, [data-cart-count]').forEach(el => {
//         el.textContent = count;
//     });
// }

// function bindHomeAddToCart() {
//     const buttons = document.querySelectorAll('.add-to-cart-btn, .shop-now-btn, [data-add-to-cart]');
//     buttons.forEach(btn => {
//         btn.addEventListener('click', async (e) => {
//             const itemType = btn.dataset.itemType;
//             const itemId = btn.dataset.itemId;

//             // If data attrs are missing, allow normal link/form behavior.
//             if (!itemType || !itemId) return;

//             e.preventDefault();
//             e.stopPropagation();

//             try {
//                 const res = await fetch(`/cart/add/${itemType}/${itemId}/`, {
//                     method: 'POST',
//                     headers: {
//                         'X-CSRFToken': getCookie('csrftoken'),
//                         'X-Requested-With': 'XMLHttpRequest',
//                         'Content-Type': 'application/json'
//                     }
//                 });
//                 const data = await res.json();

//                 if (data.success) {
//                     updateCartCountInUI(data.cart_count);
//                     showToast(data.message || 'Added to cart');
//                 } else {
//                     showToast(data.error || 'Could not add to cart');
//                 }
//             } catch (err) {
//                 showToast('Could not add to cart');
//             }
//         });
//     });
// }