/* ==========================================================================
   7X Imóveis - Global JavaScript Logic
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    initMobileNav();
    initFavorites();
    initModalEvents();
    autoHideAlerts();
});

// Mobile Navigation Toggle
function initMobileNav() {
    const toggleBtn = document.querySelector('.mobile-nav-toggle');
    const navMenu   = document.querySelector('.nav-menu');
    if (!toggleBtn || !navMenu) return;

    function openNav() {
        navMenu.classList.add('active');
        toggleBtn.innerHTML = '✕';
        toggleBtn.setAttribute('aria-expanded', 'true');
    }

    function closeNav() {
        navMenu.classList.remove('active');
        toggleBtn.innerHTML = '☰';
        toggleBtn.setAttribute('aria-expanded', 'false');
    }

    toggleBtn.addEventListener('click', () => {
        navMenu.classList.contains('active') ? closeNav() : openNav();
    });

    // Close when any nav link is clicked
    navMenu.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', closeNav);
    });

    // Close on outside click
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.site-header') && navMenu.classList.contains('active')) {
            closeNav();
        }
    });
}

// Favorites Bookmarking System (LocalStorage)
function initFavorites() {
    const favorites = JSON.parse(localStorage.getItem('7x_favorites') || '[]');

    document.querySelectorAll('.card-favorite-btn').forEach(btn => {
        const propId = btn.dataset.id;

        // Restore state
        if (favorites.includes(propId)) {
            btn.classList.add('active');
            btn.textContent = '♥';
        } else {
            btn.textContent = '♡';
        }

        btn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();

            let currentFavs = JSON.parse(localStorage.getItem('7x_favorites') || '[]');
            if (currentFavs.includes(propId)) {
                currentFavs = currentFavs.filter(id => id !== propId);
                btn.classList.remove('active');
                btn.textContent = '♡';
                showToast('Imóvel removido dos favoritos.', 'info');
            } else {
                currentFavs.push(propId);
                btn.classList.add('active');
                btn.textContent = '♥';
                showToast('Imóvel adicionado aos favoritos!', 'success');
            }
            localStorage.setItem('7x_favorites', JSON.stringify(currentFavs));
        });
    });
}

// Modal Trigger Controls
function initModalEvents() {
    document.querySelectorAll('[data-modal-target]').forEach(trigger => {
        trigger.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = trigger.getAttribute('data-modal-target');
            openModal(targetId);
        });
    });

    document.querySelectorAll('.modal-overlay').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal || e.target.classList.contains('modal-close-btn')) {
                closeModal(modal.id);
            }
        });
    });
}

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

// Toast Notifications System
function showToast(message, type = 'success') {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `alert-toast ${type}`;
    toast.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" style="background:none;border:none;color:#94a3b8;cursor:pointer;">✕</button>
    `;
    container.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 4000);
}

// Auto-hide Flask Flash Alerts after 5 seconds
function autoHideAlerts() {
    setTimeout(() => {
        document.querySelectorAll('.alert-toast').forEach(el => el.remove());
    }, 5000);
}

