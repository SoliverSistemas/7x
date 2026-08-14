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

    container.innerHTML = properties.map(p => `
        <div class="property-card">
            <div class="card-img-wrapper">
                <div class="card-badges">
                    <span class="badge badge-gold">${p.purpose}</span>
                    ${p.badge ? `<span class="badge badge-blue">${p.badge}</span>` : ''}
                </div>
                <button class="card-favorite-btn" data-id="${p.id}" title="Salvar Favorito">❤️</button>
                <img src="/static/img/${p.image}" alt="${p.title}" loading="lazy">
            </div>
            <div class="card-body">
                <div class="card-location">📍 ${p.neighborhood}, ${p.city} - ${p.state}</div>
                <h3 class="card-title">
                    <a href="/imoveis/${p.id}">${p.title}</a>
                </h3>
                <div class="card-specs">
                    <div class="card-spec-item">📐 ${p.area} m²</div>
                    <div class="card-spec-item">🛏️ ${p.bedrooms} dorms</div>
                    <div class="card-spec-item">🛁 ${p.bathrooms} banheiros</div>
                    <div class="card-spec-item">🚗 ${p.garage} vagas</div>
                </div>
                <div class="card-footer">
                    <div class="card-price-box">
                        <span class="card-price-label">Valor</span>
                        <span class="card-price-val">R$ ${p.price.toLocaleString('pt-BR', {minimumFractionDigits: 2})}</span>
                    </div>
                    <a href="/imoveis/${p.id}" class="btn btn-primary btn-sm">Ver Detalhes</a>
                </div>
            </div>
        </div>
    `).join('');

    // Re-bind favorite icons
    initFavorites();
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
