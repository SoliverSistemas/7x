/**
 * 7X — Cinematic Carousel V3
 * Navegação por setas/dots/swipe/teclado. Sem scroll-jacking.
 */

(function () {
    'use strict';

    const slides = document.querySelectorAll('.cine-slide');
    const dots   = document.querySelectorAll('.cine-dot');
    const prevBtn = document.getElementById('cine-prev');
    const nextBtn = document.getElementById('cine-next');
    const counterEl = document.getElementById('cine-counter-current');

    if (!slides.length) return;

    let current = 0;
    let isAnimating = false;
    const total = slides.length;

    /* ─── Função central: ir para um slide ───────────────────────────────── */
    function goTo(index) {
        if (isAnimating || index === current) return;
        isAnimating = true;

        const prev = current;
        current = (index + total) % total;

        // Marcar o slide anterior como "prev" (sai pela esquerda)
        slides[prev].classList.remove('active');
        slides[prev].classList.add('prev');

        // Ativar novo slide
        slides[current].classList.remove('prev');
        slides[current].classList.add('active');

        // Atualizar dots
        dots.forEach((d, i) => d.classList.toggle('active', i === current));

        // Atualizar contador
        if (counterEl) {
            counterEl.textContent = String(current + 1).padStart(2, '0');
        }

        // Limpar classe "prev" do slide anterior após a transição (0.9s)
        const cleanPrev = slides[prev];
        setTimeout(() => {
            cleanPrev.classList.remove('prev');
            // Repositiona o slide que saiu para "aguardar na direita" sem animação
            cleanPrev.style.transition = 'none';
            // Se não for o próximo provável, coloca na direita como padrão
            requestAnimationFrame(() => {
                requestAnimationFrame(() => {
                    cleanPrev.style.transition = '';
                });
            });
            isAnimating = false;
        }, 900);
    }

    function next() { goTo(current + 1); }
    function prev() { goTo(current - 1); }

    /* ─── Botões ──────────────────────────────────────────────────────────── */
    if (nextBtn) nextBtn.addEventListener('click', next);
    if (prevBtn) prevBtn.addEventListener('click', prev);

    /* ─── Dots ────────────────────────────────────────────────────────────── */
    dots.forEach((dot, i) => {
        dot.addEventListener('click', () => goTo(i));
    });

    /* ─── Teclado ─────────────────────────────────────────────────────────── */
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight') next();
        if (e.key === 'ArrowLeft')  prev();
    });

    /* ─── Swipe (Touch) ───────────────────────────────────────────────────── */
    let touchStartX = 0;
    const section = document.getElementById('cinematic-section');

    if (section) {
        section.addEventListener('touchstart', (e) => {
            touchStartX = e.touches[0].clientX;
        }, { passive: true });

        section.addEventListener('touchend', (e) => {
            const delta = touchStartX - e.changedTouches[0].clientX;
            if (Math.abs(delta) > 60) {
                delta > 0 ? next() : prev();
            }
        }, { passive: true });
    }

    /* ─── Inicializar: garantir que o slide 0 esteja ativo ───────────────── */
    slides.forEach((s, i) => {
        if (i === 0) {
            s.classList.add('active');
        } else {
            s.classList.remove('active', 'prev');
        }
    });

})();

/* ══ Bento Stat Counters ════════════════════════════════════════════════ */
(function () {
    'use strict';

    const counters = document.querySelectorAll('.bento-stat-number[data-target], .brand-stat-n[data-target]');
    if (!counters.length) return;

    function animateCounter(el) {
        const target = parseInt(el.dataset.target, 10);
        const duration = 1800;
        const start = performance.now();

        function update(now) {
            const elapsed = now - start;
            const progress = Math.min(elapsed / duration, 1);
            // Ease out cubic
            const eased = 1 - Math.pow(1 - progress, 3);
            el.textContent = Math.floor(eased * target);
            if (progress < 1) requestAnimationFrame(update);
            else el.textContent = target;
        }

        requestAnimationFrame(update);
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.4 });

    counters.forEach(el => observer.observe(el));
})();

/* ══ Brand Cinema — ativa classe visible para animações escalonadas ═════ */
(function () {
    'use strict';
    const section = document.getElementById('brand-section');
    if (!section) return;

    const io = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                section.classList.add('visible');
                io.unobserve(section);
            }
        });
    }, { threshold: 0.15 });

    io.observe(section);
})();
