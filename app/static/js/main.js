/* ==========================================================================
   7X Imóveis - Global JavaScript Logic
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    initMobileNav();
    initFavorites();
    initFavoritesDrawer();
    initSearchOverlay();
    initModalEvents();
    autoHideAlerts();
    initClickableCards();
    initPropertySliders();
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

// Favorites Bookmarking System (LocalStorage) — Versão com SVG e metadata enriquecida
function initFavorites() {
    restoreAllFavoriteButtons();

    document.querySelectorAll('.card-favorite-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            toggleFavorite(btn);
        });
    });

    updateFavoriteBadge();
}

function getFavorites() {
    return JSON.parse(localStorage.getItem('7x_favorites') || '[]');
}

function saveFavorites(favs) {
    localStorage.setItem('7x_favorites', JSON.stringify(favs));
    updateFavoriteBadge();
    window.dispatchEvent(new CustomEvent('favoritesUpdated', { detail: favs }));
}

function isFavorited(propId) {
    return getFavorites().some(f => String(f.id) === String(propId));
}

function toggleFavorite(btn) {
    const propId = btn.dataset.id;
    const card = btn.closest('.property-card');
    let favs = getFavorites();

    if (isFavorited(propId)) {
        favs = favs.filter(f => String(f.id) !== String(propId));
        btn.classList.remove('active');
        showToast('Removido dos favoritos.', 'info');
    } else {
        // Coleta metadata do card para exibir na página de favoritos
        const title   = card?.querySelector('.card-title a')?.textContent?.trim() || '';
        const price   = card?.querySelector('.card-price-val')?.textContent?.trim() || '';
        const imgSrc  = card?.querySelector('.card-img-wrapper img')?.src || '';
        const loc     = card?.querySelector('.card-location')?.textContent?.trim() || '';
        const href    = card?.dataset.href || btn.closest('a')?.href || `/imoveis/${propId}`;

        favs.push({ id: propId, title, price, imgSrc, loc, href, savedAt: Date.now() });
        btn.classList.add('active');
        showToast('Adicionado aos favoritos! ♥', 'success');
    }

    saveFavorites(favs);
}

function restoreAllFavoriteButtons() {
    document.querySelectorAll('.card-favorite-btn').forEach(btn => {
        if (isFavorited(btn.dataset.id)) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
}

function updateFavoriteBadge() {
    const count = getFavorites().length;
    document.querySelectorAll('.favorites-count-badge').forEach(badge => {
        badge.textContent = count;
        badge.style.display = count > 0 ? 'flex' : 'none';
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

// Clickable Property Cards (Torna todo o card clicável)
function initClickableCards() {
    const cards = document.querySelectorAll('.property-card');
    cards.forEach(card => {
        // Altera o cursor para mostrar que é clicável
        card.style.cursor = 'pointer';

        card.addEventListener('click', function(e) {
            // Ignora se clicou no botão de favorito, nos links ou na galeria
            if (e.target.closest('.card-favorite-btn') || e.target.closest('a') || e.target.closest('.gallery-pagination')) {
                return;
            }
            
            const href = this.dataset.href;
            if (href) {
                if (e.ctrlKey || e.metaKey || e.button === 1) {
                    window.open(href, '_blank');
                } else {
                    window.location.href = href;
                }
            }
        });
        
        // Suporte para teclado
        card.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                const link = this.querySelector('a.stretched-link');
                if (link) window.location.href = link.href;
            }
        });
    });
}

function initSearchOverlay() {
    const searchBtn = document.getElementById('header-search-btn');
    const searchOverlay = document.getElementById('searchOverlay');
    const searchCloseBtn = document.getElementById('searchCloseBtn');
    const searchInput = document.getElementById('searchOverlayInput');

    if (!searchBtn || !searchOverlay || !searchCloseBtn) return;

    searchBtn.addEventListener('click', (e) => {
        e.preventDefault();
        searchOverlay.classList.add('active');
        document.body.style.overflow = 'hidden'; // impede scroll
        setTimeout(() => {
            if (searchInput) searchInput.focus();
        }, 100);
    });

    function closeSearch() {
        searchOverlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    searchCloseBtn.addEventListener('click', closeSearch);

    // Fechar ao clicar fora do conteúdo (no fundo escuro)
    searchOverlay.addEventListener('click', (e) => {
        if (e.target === searchOverlay) {
            closeSearch();
        }
    });

    // Fechar com a tecla ESC
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && searchOverlay.classList.contains('active')) {
            closeSearch();
        }
    });
}

// ── Slider de imóveis — rolagem suave com easing + drag ─────────────────
function initPropertySliders() {
    // Easing: suavização tipo quadrática
    function easeInOutCubic(t) {
        return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    }

    function smoothScroll(el, targetX, duration) {
        const startX = el.scrollLeft;
        const delta  = targetX - startX;
        if (Math.abs(delta) < 1) return;
        let startTime = null;

        function step(timestamp) {
            if (!startTime) startTime = timestamp;
            const elapsed  = timestamp - startTime;
            const progress = Math.min(elapsed / duration, 1);
            el.scrollLeft  = startX + delta * easeInOutCubic(progress);
            if (progress < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
    }

    function updateButtons(slider, prevBtn, nextBtn) {
        if (prevBtn) prevBtn.disabled = slider.scrollLeft <= 2;
        if (nextBtn) nextBtn.disabled = slider.scrollLeft + slider.clientWidth >= slider.scrollWidth - 2;
    }

    document.querySelectorAll('.properties-slider-wrapper').forEach(wrapper => {
        const slider  = wrapper.querySelector('.properties-slider');
        const prevBtn = wrapper.querySelector('.slider-nav-btn.prev');
        const nextBtn = wrapper.querySelector('.slider-nav-btn.next');
        if (!slider) return;

        // Atualiza estado inicial dos botões
        updateButtons(slider, prevBtn, nextBtn);
        slider.addEventListener('scroll', () => updateButtons(slider, prevBtn, nextBtn), { passive: true });

        // Calcula quanto rolar: exatamente 1 largura de card + gap
        function getScrollStep() {
            const card = slider.querySelector('.property-card');
            if (!card) return slider.clientWidth * 0.75;
            const style = getComputedStyle(slider);
            const gap   = parseFloat(style.gap) || 24;
            return card.offsetWidth + gap;
        }

        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                smoothScroll(slider, slider.scrollLeft - getScrollStep() * 3, 550);
            });
        }
        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                smoothScroll(slider, slider.scrollLeft + getScrollStep() * 3, 550);
            });
        }

        // ── Drag-to-scroll (arrastar com o mouse) ──────────────────────────
        let isDragging = false;
        let startX, startScrollLeft, velX = 0, lastX, rafId;

        slider.addEventListener('mousedown', e => {
            if (e.button !== 0) return;
            isDragging    = true;
            startX        = e.pageX;
            startScrollLeft = slider.scrollLeft;
            lastX         = e.pageX;
            velX          = 0;
            slider.classList.add('is-dragging');
            cancelAnimationFrame(rafId);
        });

        document.addEventListener('mousemove', e => {
            if (!isDragging) return;
            const dx      = e.pageX - startX;
            velX          = e.pageX - lastX;
            lastX         = e.pageX;
            slider.scrollLeft = startScrollLeft - dx;
        });

        document.addEventListener('mouseup', () => {
            if (!isDragging) return;
            isDragging = false;
            slider.classList.remove('is-dragging');
            // Inércia suave ao soltar
            let velocity = -velX * 1.8;
            function inertia() {
                if (Math.abs(velocity) < 0.5) return;
                slider.scrollLeft += velocity;
                velocity *= 0.9;
                rafId = requestAnimationFrame(inertia);
            }
            rafId = requestAnimationFrame(inertia);
        });

        // Previne que links/cards sejam ativados durante o drag
        slider.addEventListener('click', e => {
            if (Math.abs(slider.scrollLeft - startScrollLeft) > 5) {
                e.preventDefault();
                e.stopPropagation();
            }
        }, true);
    });
}

/* ── Favorites Side Drawer ──────────────────────────────────────────────── */
function initFavoritesDrawer() {
    const btn      = document.getElementById('header-favorites-btn');
    const drawer   = document.getElementById('favDrawer');
    const overlay  = document.getElementById('favDrawerOverlay');
    const closeBtn = document.getElementById('favDrawerClose');
    if (!btn || !drawer) return;

    function openDrawer() {
        renderFavDrawer();
        drawer.classList.add('open');
        overlay.classList.add('open');
        document.body.style.overflow = 'hidden';
    }

    function closeDrawer() {
        drawer.classList.remove('open');
        overlay.classList.remove('open');
        document.body.style.overflow = '';
    }

    btn.addEventListener('click', () => {
        drawer.classList.contains('open') ? closeDrawer() : openDrawer();
    });

    closeBtn?.addEventListener('click', closeDrawer);
    overlay?.addEventListener('click', closeDrawer);

    // Close on Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && drawer.classList.contains('open')) closeDrawer();
    });

    // Re-render when favorites change
    window.addEventListener('favoritesUpdated', () => {
        if (drawer.classList.contains('open')) renderFavDrawer();
        syncFavBtn();
    });

    syncFavBtn();
}

function syncFavBtn() {
    const btn = document.getElementById('header-favorites-btn');
    if (!btn) return;
    const count = getFavorites().length;
    if (count > 0) {
        btn.classList.add('has-favorites');
    } else {
        btn.classList.remove('has-favorites');
    }
    updateFavoriteBadge();
}

function renderFavDrawer() {
    const body = document.getElementById('favDrawerBody');
    if (!body) return;
    const favs = getFavorites();

    if (favs.length === 0) {
        body.innerHTML = `
            <div class="fav-drawer-empty">
                <svg width="52" height="52" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
                </svg>
                <p>Nenhum imóvel nos favoritos ainda.<br>Clique no ♡ nos cards para salvar.</p>
                <a href="/imoveis/">Ver Catálogo &rarr;</a>
            </div>
        `;
        return;
    }

    body.innerHTML = favs.map(fav => `
        <a class="fav-item" href="${fav.href || '#'}">
            ${ fav.imgSrc
                ? `<img class="fav-item-img" src="${fav.imgSrc}" alt="${fav.title}" loading="lazy">`
                : `<div class="fav-item-img-placeholder">
                       <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="18" height="18"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
                   </div>`
            }
            <div class="fav-item-info">
                <div class="fav-item-title">${fav.title || 'Imóvel Salvo'}</div>
                <div class="fav-item-loc">${fav.loc ? fav.loc.replace(/^\s*[\u{1F4CD}]\s*/u, '').trim() : ''}</div>
                <div class="fav-item-price">${fav.price || ''}</div>
            </div>
            <button class="fav-item-remove" data-id="${fav.id}" title="Remover" aria-label="Remover dos favoritos">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
        </a>
    `).join('');

    // Wire remove buttons (prevent event bubbling to the link)
    body.querySelectorAll('.fav-item-remove').forEach(removeBtn => {
        removeBtn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            const id = removeBtn.dataset.id;
            let favs = getFavorites().filter(f => String(f.id) !== String(id));
            saveFavorites(favs);
            renderFavDrawer();
            // Sync heart buttons on page
            document.querySelectorAll(`.card-favorite-btn[data-id="${id}"]`).forEach(b => b.classList.remove('active'));
            showToast('Removido dos favoritos.', 'info');
        });
    });
}
