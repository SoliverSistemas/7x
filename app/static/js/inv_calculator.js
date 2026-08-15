/**
 * 7X Patrimonial — Investment Intelligence Calculator
 * ────────────────────────────────────────────────────
 * Features:
 *  • Golden particle field (canvas) — performance-aware, respects prefers-reduced-motion
 *  • SVG gauge with animated needle and dashoffset arc
 *  • Canvas multi-line projection chart (Imóvel vs Poupança vs Ibovespa)
 *    with mousemove tooltip
 *  • Real-time KPI counters with animated number transitions
 *  • Custom slider fill track synced to range input value
 *  • Rental toggle + yield sub-slider
 *  • Property type chips (each has its own appreciation rate)
 *  • CTA button auto-updates with current simulation values
 *
 * All calculations are illustrative / educational; not financial advice.
 */

(function () {
    'use strict';

    /* ─────────────────────────────────────────────────────────────────────
       CONFIG & CONSTANTS
    ───────────────────────────────────────────────────────────────────── */
    const POUPANCA_RATE   = 0.0760;  // ~7.6% a.a. (Selic-bound, simplified)
    const IBOVESPA_RATE   = 0.1180;  // ~11.8% a.a. (historical mean, simplified)
    const PRIMARY_COLOR   = '#c9ac77';
    const PRIMARY_LIGHT   = '#f0d98a';
    const GRAY_COLOR      = '#6b7280';
    const BLUE_COLOR      = '#3b82f6';

    // Arc constants: semicircle M 20 110 A 90 90 0 0 1 180 110
    // Arc perimeter (half circle r=90): π * 90 ≈ 282.74
    const ARC_LEN = Math.PI * 90; // ≈ 282.74

    /* ─────────────────────────────────────────────────────────────────────
       STATE
    ───────────────────────────────────────────────────────────────────── */
    let state = {
        price:       2_500_000,
        entrada:     30,
        horizon:     5,
        rentalOn:    true,
        yieldMonthly: 0.50,   // % mensal
        apprecRate:  12.4,    // % a.a. — set by type chip
    };

    // Animation frame handles
    let particleRAF = null;
    let chartRAF    = null;
    let kpiTimers   = {};

    /* ─────────────────────────────────────────────────────────────────────
       DOM REFS (populated on init)
    ───────────────────────────────────────────────────────────────────── */
    const $ = id => document.getElementById(id);
    let els = {};

    /* ─────────────────────────────────────────────────────────────────────
       UTILS
    ───────────────────────────────────────────────────────────────────── */
    function formatBRL(v) {
        if (v >= 1_000_000) return `R$ ${(v / 1_000_000).toFixed(2).replace('.', ',')}M`;
        if (v >= 1_000)     return `R$ ${(v / 1_000).toFixed(0)}k`;
        return `R$ ${v.toFixed(0)}`;
    }

    function formatBRLFull(v) {
        return 'R$ ' + Math.round(v).toLocaleString('pt-BR');
    }

    function lerp(a, b, t) { return a + (b - a) * t; }

    function clamp(v, min, max) { return Math.min(Math.max(v, min), max); }

    function easeOutCubic(t) { return 1 - Math.pow(1 - t, 3); }

    /* ─────────────────────────────────────────────────────────────────────
       PARTICLE SYSTEM (canvas background)
    ───────────────────────────────────────────────────────────────────── */
    function initParticles() {
        const canvas = $('inv-particles-canvas');
        if (!canvas) return;

        // Skip animation if user prefers reduced motion
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

        const ctx = canvas.getContext('2d');
        let W, H, particles;

        const PARTICLE_COUNT = window.innerWidth < 768 ? 40 : 80;

        function resize() {
            const rect = canvas.parentElement.getBoundingClientRect();
            W = canvas.width  = rect.width;
            H = canvas.height = rect.height;
            buildParticles();
        }

        function buildParticles() {
            particles = Array.from({ length: PARTICLE_COUNT }, () => ({
                x:     Math.random() * W,
                y:     Math.random() * H,
                r:     Math.random() * 1.8 + 0.4,
                speed: Math.random() * 0.35 + 0.1,
                angle: Math.random() * Math.PI * 2,
                drift: (Math.random() - 0.5) * 0.008,
                alpha: Math.random() * 0.5 + 0.15,
                pulse: Math.random() * Math.PI * 2,
            }));
        }

        function tick() {
            ctx.clearRect(0, 0, W, H);

            particles.forEach(p => {
                // Move
                p.angle += p.drift;
                p.x += Math.cos(p.angle) * p.speed;
                p.y -= p.speed * 0.6;
                p.pulse += 0.025;

                // Wrap
                if (p.x < -5) p.x = W + 5;
                if (p.x > W + 5) p.x = -5;
                if (p.y < -5) { p.y = H + 5; p.x = Math.random() * W; }

                const alpha = p.alpha * (0.6 + 0.4 * Math.sin(p.pulse));

                // Draw gold dot
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(201, 172, 119, ${alpha})`;
                ctx.fill();
            });

            particleRAF = requestAnimationFrame(tick);
        }

        resize();
        window.addEventListener('resize', resize);

        // Only run particles when section is visible
        const observer = new IntersectionObserver(entries => {
            entries.forEach(e => {
                if (e.isIntersecting) {
                    if (!particleRAF) tick();
                } else {
                    cancelAnimationFrame(particleRAF);
                    particleRAF = null;
                }
            });
        }, { threshold: 0.05 });

        observer.observe(canvas.parentElement);
    }

    /* ─────────────────────────────────────────────────────────────────────
       SLIDER FILL SYNC
    ───────────────────────────────────────────────────────────────────── */
    function updateFill(sliderId, fillId) {
        const slider = $(sliderId);
        const fill   = $(fillId);
        if (!slider || !fill) return;

        const pct = (slider.value - slider.min) / (slider.max - slider.min) * 100;
        fill.style.width = pct + '%';
    }

    function initSliderFills() {
        [
            ['inv-price',   'inv-price-fill'],
            ['inv-entrada', 'inv-entrada-fill'],
            ['inv-horizon', 'inv-horizon-fill'],
            ['inv-yield',   'inv-yield-fill'],
        ].forEach(([sid, fid]) => updateFill(sid, fid));
    }

    /* ─────────────────────────────────────────────────────────────────────
       GAUGE
    ───────────────────────────────────────────────────────────────────── */
    function injectGaugeGradient() {
        const svg = document.querySelector('.inv-gauge-svg');
        if (!svg || svg.querySelector('#inv-gauge-gradient')) return;

        const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
        defs.innerHTML = `
            <linearGradient id="inv-gauge-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%"   stop-color="#ef4444"/>
                <stop offset="45%"  stop-color="#f59e0b"/>
                <stop offset="100%" stop-color="#10b981"/>
            </linearGradient>`;
        svg.insertBefore(defs, svg.firstChild);
    }

    /**
     * Update the gauge arc (stroke-dashoffset) and needle rotation.
     * @param {number} pct  0..1 representing progress across the semicircle
     */
    function setGauge(pct) {
        const arc    = $('inv-gauge-arc');
        const needle = $('inv-gauge-needle');
        if (!arc || !needle) return;

        const clamped = clamp(pct, 0, 1);
        const offset  = ARC_LEN * (1 - clamped);
        arc.style.strokeDashoffset = offset;

        // Needle: -90deg = far left (0%), +90deg = far right (100%)
        const deg = -90 + clamped * 180;
        needle.style.transform = `rotate(${deg}deg)`;
    }

    /* ─────────────────────────────────────────────────────────────────────
       ANIMATED COUNTER
    ───────────────────────────────────────────────────────────────────── */
    function animateValue(el, fromVal, toVal, duration, formatter) {
        if (!el) return;
        const id   = el.id;
        if (kpiTimers[id]) cancelAnimationFrame(kpiTimers[id]);

        const start = performance.now();

        function step(now) {
            const t   = Math.min((now - start) / duration, 1);
            const val = lerp(fromVal, toVal, easeOutCubic(t));
            el.textContent = formatter(val);
            if (t < 1) kpiTimers[id] = requestAnimationFrame(step);
        }

        kpiTimers[id] = requestAnimationFrame(step);
    }

    /* ─────────────────────────────────────────────────────────────────────
       PROJECTION CHART (Canvas)
    ───────────────────────────────────────────────────────────────────── */
    let projectionData = null; // { years, imovel, poupanca, ibov }
    let hoveredYear    = null;

    function buildProjectionData() {
        const years    = [];
        const imovel   = [];
        const poupanca = [];
        const ibov     = [];

        const basePrice   = state.price;
        const apprecAnnual = state.apprecRate / 100;
        const yieldAnnual  = state.rentalOn ? (state.yieldMonthly / 100) * 12 : 0;
        const n = state.horizon;

        for (let y = 0; y <= n; y++) {
            const imovelVal = basePrice * Math.pow(1 + apprecAnnual, y)
                            + (state.rentalOn ? basePrice * yieldAnnual * y : 0);
            years.push(y);
            imovel.push(imovelVal);
            poupanca.push(basePrice * Math.pow(1 + POUPANCA_RATE, y));
            ibov.push(basePrice * Math.pow(1 + IBOVESPA_RATE, y));
        }

        return { years, imovel, poupanca, ibov };
    }

    function drawProjectionChart(data) {
        const canvas = $('inv-projection-canvas');
        if (!canvas) return;

        const container = canvas.parentElement;
        const dpr = window.devicePixelRatio || 1;
        const W   = container.clientWidth;
        const H   = container.clientHeight;

        canvas.width  = W * dpr;
        canvas.height = H * dpr;
        canvas.style.width  = W + 'px';
        canvas.style.height = H + 'px';

        const ctx = canvas.getContext('2d');
        ctx.scale(dpr, dpr);

        const PAD = { top: 16, right: 16, bottom: 32, left: 56 };
        const cW  = W - PAD.left - PAD.right;
        const cH  = H - PAD.top  - PAD.bottom;

        // Find global max
        const allVals = [...data.imovel, ...data.poupanca, ...data.ibov];
        const maxVal  = Math.max(...allVals);
        const minVal  = data.poupanca[0] * 0.95;

        function xPos(i) { return PAD.left + (i / (data.years.length - 1)) * cW; }
        function yPos(v) { return PAD.top + cH - ((v - minVal) / (maxVal - minVal)) * cH; }

        // Grid lines
        const GRID_LINES = 4;
        ctx.strokeStyle = 'rgba(201,172,119,0.06)';
        ctx.lineWidth = 1;

        for (let g = 0; g <= GRID_LINES; g++) {
            const y = PAD.top + (g / GRID_LINES) * cH;
            ctx.beginPath();
            ctx.moveTo(PAD.left, y);
            ctx.lineTo(W - PAD.right, y);
            ctx.stroke();

            const val = maxVal - (g / GRID_LINES) * (maxVal - minVal);
            ctx.fillStyle = 'rgba(107,101,96,0.8)';
            ctx.font = '10px Inter, sans-serif';
            ctx.textAlign = 'right';
            ctx.fillText(formatBRL(val), PAD.left - 6, y + 3.5);
        }

        // Year labels on X axis
        ctx.fillStyle = 'rgba(107,101,96,0.8)';
        ctx.textAlign = 'center';
        data.years.forEach((yr, i) => {
            if (data.years.length > 12 && yr % 2 !== 0 && yr !== data.years[data.years.length - 1]) return;
            ctx.fillText(yr === 0 ? 'Hoje' : `${yr}a`, xPos(i), H - PAD.bottom + 16);
        });

        // Draw lines
        function drawLine(arr, color, dashed) {
            ctx.beginPath();
            ctx.strokeStyle = color;
            ctx.lineWidth   = dashed ? 1.5 : 2.5;
            if (dashed) ctx.setLineDash([5, 4]);
            else        ctx.setLineDash([]);

            arr.forEach((v, i) => {
                const x = xPos(i);
                const y = yPos(v);
                i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
            });
            ctx.stroke();
        }

        // Gradient fill under imovel line
        ctx.beginPath();
        data.imovel.forEach((v, i) => {
            const x = xPos(i);
            const y = yPos(v);
            i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        });
        ctx.lineTo(xPos(data.imovel.length - 1), H - PAD.bottom);
        ctx.lineTo(PAD.left, H - PAD.bottom);
        ctx.closePath();

        const grad = ctx.createLinearGradient(0, PAD.top, 0, H - PAD.bottom);
        grad.addColorStop(0,   'rgba(201,172,119,0.22)');
        grad.addColorStop(1,   'rgba(201,172,119,0.0)');
        ctx.fillStyle = grad;
        ctx.fill();

        drawLine(data.ibov,     BLUE_COLOR,    true);
        drawLine(data.poupanca, GRAY_COLOR,    true);
        drawLine(data.imovel,   PRIMARY_COLOR, false);

        // Hovered year indicator
        if (hoveredYear !== null) {
            const idx = hoveredYear;
            const x   = xPos(idx);

            ctx.beginPath();
            ctx.strokeStyle = 'rgba(201,172,119,0.35)';
            ctx.lineWidth   = 1;
            ctx.setLineDash([3, 3]);
            ctx.moveTo(x, PAD.top);
            ctx.lineTo(x, H - PAD.bottom);
            ctx.stroke();
            ctx.setLineDash([]);

            [[data.imovel, PRIMARY_COLOR], [data.poupanca, GRAY_COLOR], [data.ibov, BLUE_COLOR]].forEach(([arr, color]) => {
                ctx.beginPath();
                ctx.arc(x, yPos(arr[idx]), 4.5, 0, Math.PI * 2);
                ctx.fillStyle   = color;
                ctx.strokeStyle = '#171a1c';
                ctx.lineWidth   = 2;
                ctx.fill();
                ctx.stroke();
            });
        }
    }

    function initChartInteraction() {
        const canvas  = $('inv-projection-canvas');
        const tooltip = $('inv-chart-tooltip');
        if (!canvas || !tooltip) return;

        canvas.addEventListener('mousemove', e => {
            if (!projectionData) return;
            const rect = canvas.getBoundingClientRect();
            const PAD_LEFT  = 56;
            const PAD_RIGHT = 16;
            const cW = rect.width - PAD_LEFT - PAD_RIGHT;
            const relX = e.clientX - rect.left - PAD_LEFT;

            const n       = projectionData.years.length - 1;
            const fracIdx = clamp(relX / cW, 0, 1) * n;
            const idx     = Math.round(fracIdx);

            if (idx < 0 || idx > n) { hoveredYear = null; return; }

            hoveredYear = idx;
            drawProjectionChart(projectionData);

            const yr = projectionData.years[idx];
            const im = projectionData.imovel[idx];
            const po = projectionData.poupanca[idx];
            const ib = projectionData.ibov[idx];

            tooltip.innerHTML =
                `<strong>Ano ${yr}</strong><br>` +
                `<span style="color:${PRIMARY_COLOR}">▲ Imóvel 7X: ${formatBRL(im)}</span><br>` +
                `<span style="color:${BLUE_COLOR}">▲ Ibovespa: ${formatBRL(ib)}</span><br>` +
                `<span style="color:${GRAY_COLOR}">▲ Poupança: ${formatBRL(po)}</span>`;

            const cx     = e.clientX - rect.left;
            const cy     = e.clientY - rect.top;
            const tipW   = 180;
            let   tipX   = cx + 12;
            if (tipX + tipW > rect.width) tipX = cx - tipW - 12;
            tooltip.style.left = tipX + 'px';
            tooltip.style.top  = (cy - 10) + 'px';
            tooltip.classList.add('visible');
        });

        canvas.addEventListener('mouseleave', () => {
            hoveredYear = null;
            tooltip.classList.remove('visible');
            drawProjectionChart(projectionData);
        });
    }

    /* ─────────────────────────────────────────────────────────────────────
       CORE CALCULATION & UI UPDATE
    ───────────────────────────────────────────────────────────────────── */
    let prevKPIs = { valorizacao: 0, rentalTotal: 0, patrimonio: 0 };

    function calculate() {
        const p          = state.price;
        const entrada    = p * (state.entrada / 100);
        const n          = state.horizon;
        const apprecFrac = state.apprecRate / 100;

        const futureVal   = p * Math.pow(1 + apprecFrac, n);
        const valorizacao = futureVal - p;

        const rentalYield  = state.rentalOn ? (state.yieldMonthly / 100) * 12 : 0;
        const rentalTotal  = state.rentalOn ? p * rentalYield * n : 0;

        const totalReturn = valorizacao + rentalTotal;
        const roi         = totalReturn / entrada;
        const roiPct      = roi * 100;

        const patrimonio  = futureVal + rentalTotal;

        let breakeven = null;
        if (state.rentalOn && rentalYield > 0) {
            breakeven = entrada / (p * rentalYield);
        }

        /* Gauge */
        const gaugeMax = 150;
        setGauge(clamp(roiPct / gaugeMax, 0, 1));

        animateValue($('inv-roi-display'), parseFloat($('inv-roi-display').dataset.prev || 0), roiPct, 600, v => {
            return v >= 0 ? `+${v.toFixed(0)}%` : `${v.toFixed(0)}%`;
        });
        $('inv-roi-display').dataset.prev = roiPct;

        /* KPIs */
        animateValue($('inv-kpi-valorizacao'),    prevKPIs.valorizacao, valorizacao,  600, formatBRLFull);
        animateValue($('inv-kpi-rental-total'),   prevKPIs.rentalTotal, rentalTotal,  600,
            v => state.rentalOn ? formatBRLFull(v) : '—');
        animateValue($('inv-kpi-patrimonio'),     prevKPIs.patrimonio,  patrimonio,   600, formatBRLFull);

        const beEl = $('inv-kpi-breakeven');
        if (beEl) {
            beEl.textContent = (state.rentalOn && breakeven !== null)
                ? `${breakeven.toFixed(1)} anos`
                : '—';
        }

        prevKPIs = { valorizacao, rentalTotal, patrimonio };

        const badge = $('inv-chart-apprec-badge');
        if (badge) badge.textContent = `+${state.apprecRate.toFixed(1)}% a.a.`;

        projectionData = buildProjectionData();
        drawProjectionChart(projectionData);
    }

    /* ─────────────────────────────────────────────────────────────────────
       SLIDER BINDING
    ───────────────────────────────────────────────────────────────────── */
    function bindSlider(sliderId, fillId, displayId, onChange) {
        const slider  = $(sliderId);
        const display = $(displayId);
        if (!slider) return;

        function update() {
            updateFill(sliderId, fillId);
            if (display && onChange) display.textContent = onChange(slider.value);
            calculate();
        }

        slider.addEventListener('input', update);
        update();
    }

    /* ─────────────────────────────────────────────────────────────────────
       INIT
    ───────────────────────────────────────────────────────────────────── */
    function init() {
        const section = document.getElementById('inv-intel');
        if (!section) return;

        injectGaugeGradient();
        initParticles();
        initChartInteraction();
        initSliderFills();

        bindSlider('inv-price', 'inv-price-fill', 'inv-price-display', v => {
            state.price = +v;
            const m = +v / 1_000_000;
            if (m >= 1) return `R$ ${m.toFixed(1).replace('.', ',')}M`;
            return `R$ ${(+v / 1000).toFixed(0)}k`;
        });

        bindSlider('inv-entrada', 'inv-entrada-fill', 'inv-entrada-display', v => {
            state.entrada = +v;
            return `${v}%`;
        });

        bindSlider('inv-horizon', 'inv-horizon-fill', 'inv-horizon-display', v => {
            state.horizon = +v;
            return `${v} ${+v === 1 ? 'ano' : 'anos'}`;
        });

        bindSlider('inv-yield', 'inv-yield-fill', 'inv-yield-display', v => {
            state.yieldMonthly = +v;
            return `${(+v).toFixed(2).replace('.', ',')}%`;
        });

        const toggleBtn    = $('inv-rental-toggle');
        const rentalInputs = $('inv-rental-inputs');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => {
                state.rentalOn = !state.rentalOn;
                toggleBtn.classList.toggle('active', state.rentalOn);
                toggleBtn.setAttribute('aria-checked', state.rentalOn);
                if (rentalInputs) rentalInputs.classList.toggle('collapsed', !state.rentalOn);
                calculate();
            });
        }

        document.querySelectorAll('.inv-type-chip').forEach(chip => {
            chip.addEventListener('click', () => {
                document.querySelectorAll('.inv-type-chip').forEach(c => {
                    c.classList.remove('active');
                    c.setAttribute('aria-checked', 'false');
                });
                chip.classList.add('active');
                chip.setAttribute('aria-checked', 'true');
                state.apprecRate = parseFloat(chip.dataset.apprec);
                calculate();
            });
        });

        window.addEventListener('resize', () => {
            if (projectionData) drawProjectionChart(projectionData);
        });

        calculate();
    }

    /* ─────────────────────────────────────────────────────────────────────
       BOOT
    ───────────────────────────────────────────────────────────────────── */
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
