/* ==========================================================================
   7X Imóveis - Property Catalog & Interactive Features JS
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    initCatalogFilters();
    initFinancingCalculator();
    initVisitScheduler();
});

// Dynamic Property Catalog Filtering
function initCatalogFilters() {
    const filterForm = document.getElementById('catalog-filter-form');
    const container = document.getElementById('properties-container');
    const countDisplay = document.getElementById('results-count');

    if (!filterForm || !container) return;

    // Listen to form input & change events
    const triggerSearch = debounce(() => {
        const formData = new FormData(filterForm);
        const params = new URLSearchParams(formData).toString();

        fetch(`/api/properties?${params}`)
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    renderProperties(data.properties, container);
                    if (countDisplay) {
                        countDisplay.textContent = `${data.count} imóveis encontrados`;
                    }
                }
            })
            .catch(err => console.error('Erro na filtragem:', err));
    }, 300);

    filterForm.querySelectorAll('input, select').forEach(input => {
        input.addEventListener('change', triggerSearch);
        if (input.type === 'text') {
            input.addEventListener('keyup', triggerSearch);
        }
    });
}

function renderProperties(properties, container) {
    if (!properties || properties.length === 0) {
        container.innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; padding: 4rem 1rem;">
                <h3 style="margin-bottom: 0.5rem;">Nenhum imóvel encontrado</h3>
                <p style="color: var(--text-secondary);">Tente ajustar seus filtros de busca para encontrar mais opções.</p>
            </div>
        `;
        return;
    }

    const formatCurrency = (val) => {
        if (!val && val !== 0) return '—';
        return 'R$ ' + Number(val).toLocaleString('pt-BR', { minimumFractionDigits: 2 });
    };

    container.innerHTML = properties.map(p => `
        <div class="property-card" data-href="/imoveis/${p.id}">
            <div class="card-img-wrapper">
                <div class="card-badges">
                    <span class="badge badge-gold">${p.purpose || ''}</span>
                    ${p.badge ? `<span class="badge badge-blue">${p.badge}</span>` : ''}
                </div>
                <button class="card-favorite-btn" data-id="${p.id}" title="Salvar Favorito" aria-label="Salvar nos favoritos">
                    <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
                </button>
                <img src="/static/img/${p.image}" alt="${p.title}" loading="lazy">
                <div class="card-price-overlay">
                    <span class="card-price-label">${p.purpose === 'Aluguel' ? 'Aluguel / mês' : 'Valor'}</span>
                    <span class="card-price-val">${formatCurrency(p.price)}</span>
                </div>
            </div>
            <div class="card-body">
                <div class="card-location">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                    ${p.neighborhood || ''}, ${p.city || ''}
                </div>
                <h3 class="card-title">
                    <a href="/imoveis/${p.id}">${p.title}</a>
                </h3>
                <div class="card-specs">
                    ${p.area ? `
                    <div class="card-spec-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="14" height="14"><path d="M3 3h7v7H3zM14 3h7v7h-7zM14 14h7v7h-7zM3 14h7v7H3z"/></svg>
                        <span>${p.area} m²</span>
                    </div>` : ''}
                    ${p.bedrooms ? `
                    <div class="card-spec-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="14" height="14"><path d="M3 14h18v6H3z"/><path d="M3 14V8a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v6"/><path d="M7 10h10"/></svg>
                        <span>${p.bedrooms} dorms</span>
                    </div>` : ''}
                    ${p.suites ? `
                    <div class="card-spec-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="14" height="14"><path d="M5 12H3l9-9 9 9h-2"/><path d="M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-7"/></svg>
                        <span>${p.suites} suítes</span>
                    </div>` : ''}
                    ${p.garage ? `
                    <div class="card-spec-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="14" height="14"><rect x="2" y="7" width="20" height="14"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
                        <span>${p.garage} vagas</span>
                    </div>` : ''}
                </div>
                <div class="card-info-chips">
                    ${p.is_financeable ? '<span class="card-chip">Financiável</span>' : ''}
                    ${p.accepts_exchange ? '<span class="card-chip">Aceita Troca</span>' : ''}
                    ${p.furnished && p.furnished !== 'Não mobiliado' ? '<span class="card-chip">Mobiliado</span>' : ''}
                </div>
                <div class="card-footer">
                    ${p.condo_fee ? `
                    <div style="font-size:0.72rem; color:var(--text-muted); line-height:1.3;">
                        <span style="display:block; text-transform:uppercase; letter-spacing:0.05em;">Condomínio</span>
                        <span style="font-weight:600; color:var(--text-secondary);">${formatCurrency(p.condo_fee)}</span>
                    </div>` : '<div></div>'}
                    <a href="/imoveis/${p.id}" class="card-cta-btn">
                        Ver detalhes
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="12" height="12"><polyline points="9 18 15 12 9 6"/></svg>
                    </a>
                </div>
            </div>
        </div>
    `).join('');

    // Re-bind favorites & clickable cards after DOM update
    if (typeof restoreAllFavoriteButtons === 'function') restoreAllFavoriteButtons();
    if (typeof initFavorites === 'function') {
        document.querySelectorAll('.card-favorite-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                if (typeof toggleFavorite === 'function') toggleFavorite(btn);
            });
        });
    }
}

// Financing / Mortgage Calculator
function initFinancingCalculator() {
    const calcForm = document.getElementById('financing-calc-form');
    const resultBox = document.getElementById('calc-results-box');

    if (!calcForm) return;

    calcForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const propVal = parseFloat(document.getElementById('calc-prop-val').value) || 0;
        const downPayment = parseFloat(document.getElementById('calc-down-payment').value) || 0;
        const years = parseInt(document.getElementById('calc-years').value) || 30;

        fetch('/api/calculate-financing', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                property_value: propVal,
                down_payment: downPayment,
                years: years
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success' && resultBox) {
                resultBox.style.display = 'block';
                document.getElementById('res-installment').textContent = `R$ ${data.monthly_installment.toLocaleString('pt-BR', {minimumFractionDigits: 2})}`;
                document.getElementById('res-financed').textContent = `R$ ${data.financed_amount.toLocaleString('pt-BR', {minimumFractionDigits: 2})}`;
                document.getElementById('res-total-interest').textContent = `R$ ${data.total_interest.toLocaleString('pt-BR', {minimumFractionDigits: 2})}`;
            } else {
                showToast(data.message || 'Erro no cálculo', 'error');
            }
        })
        .catch(err => console.error('Erro na calculadora:', err));
    });
}

// Visit Scheduler Form
function initVisitScheduler() {
    const visitForm = document.getElementById('schedule-visit-form');
    if (!visitForm) return;

    visitForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const formData = new FormData(visitForm);

        fetch('/api/schedule-visit', {
            method: 'POST',
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success') {
                showToast(data.message, 'success');
                closeModal('scheduleVisitModal');
                visitForm.reset();
            } else {
                showToast(data.message, 'error');
            }
        })
        .catch(err => console.error('Erro no agendamento:', err));
    });
}

// Debounce helper
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
