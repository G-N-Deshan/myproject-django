
(() => {
    const tabButtons = document.querySelectorAll('.wishlist-tab');
    const tabPanes = document.querySelectorAll('.wishlist-tab-pane');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabName = button.dataset.tab;

            tabButtons.forEach(btn => {
                btn.classList.remove('is-active');
                btn.setAttribute('aria-selected', 'false');
            });

            tabPanes.forEach(pane => {
                pane.classList.remove('is-active');
                pane.style.display = 'none';
            });

            button.classList.add('is-active');
            button.setAttribute('aria-selected', 'true');

            const activePane = document.getElementById(`tab-${tabName}`);
            if (activePane) {
                activePane.classList.add('is-active');
                activePane.style.display = 'block';
            }
        });
    });

    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.3s ease';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 4000);
    });
})();