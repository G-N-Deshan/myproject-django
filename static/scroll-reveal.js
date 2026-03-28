
(function () {
    'use strict';

    if (!('IntersectionObserver' in window)) return;

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
    );

    function observeElements() {
        document.querySelectorAll('[data-reveal]:not(.revealed)').forEach((el) => {
            observer.observe(el);
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', observeElements);
    } else {
        observeElements();
    }

    if ('MutationObserver' in window) {
        const mo = new MutationObserver((mutations) => {
            mutations.forEach((m) => {
                m.addedNodes.forEach((node) => {
                    if (node.nodeType === 1) {
                        if (node.hasAttribute && node.hasAttribute('data-reveal')) {
                            observer.observe(node);
                        }
                        if (node.querySelectorAll) {
                            node.querySelectorAll('[data-reveal]:not(.revealed)').forEach((el) => {
                                observer.observe(el);
                            });
                        }
                    }
                });
            });
        });
        mo.observe(document.body || document.documentElement, { childList: true, subtree: true });
    }
})();
