/* ==========================================================================
   7X Imóveis - Advanced GSAP Animations + Counter + Reveal System
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    if (typeof gsap !== 'undefined') {
        if (typeof ScrollTrigger !== 'undefined') {
            gsap.registerPlugin(ScrollTrigger);
        }

        initHeroAnimations();
        initScrollReveal();
        initHoverEffects();
        initStatCounters();
        initHeaderScroll();
    }
});

// ── 1. Hero Entrance Animations ─────────────────────────────────────────
function initHeroAnimations() {
    // Only run if hero content exists on this page
    const heroTitle = document.querySelector('.hero-title');
    if (!heroTitle) return;

    const heroTl = gsap.timeline({ defaults: { ease: 'power3.out', duration: 1 } });

    heroTl.from('.site-header', {
        y: -100,
        opacity: 0,
        duration: 0.8
    });

    const heroBadge = document.querySelector('.hero-content .badge');
    if (heroBadge) {
        heroTl.from(heroBadge, { scale: 0.8, opacity: 0, duration: 0.5 }, '-=0.3');
    }

    heroTl.from(heroTitle, { y: 40, opacity: 0, duration: 1 }, '-=0.3');

    const heroSub = document.querySelector('.hero-subtitle');
    if (heroSub) {
        heroTl.from(heroSub, { y: 20, opacity: 0, duration: 0.8 }, '-=0.6');
    }

    const heroSearch = document.querySelector('.hero-search-box');
    if (heroSearch) {
        heroTl.from(heroSearch, { y: 50, opacity: 0, scale: 0.96, duration: 0.9 }, '-=0.5');
    }

    const heroHint = document.querySelector('.hero-scroll-hint');
    if (heroHint) {
        heroTl.from(heroHint, { opacity: 0, duration: 0.5 }, '-=0.3');
    }
}

// ── 2. ScrollTrigger Reveal System ──────────────────────────────────────
function initScrollReveal() {
    if (typeof ScrollTrigger === 'undefined') return;

    // Reveal elements with .reveal class
    gsap.utils.toArray('.reveal').forEach((el, i) => {
        gsap.from(el, {
            scrollTrigger: {
                trigger: el,
                start: 'top 88%',
                toggleActions: 'play none none none'
            },
            y: 40,
            opacity: 0,
            duration: 0.7,
            delay: (i % 4) * 0.1, // stagger within viewport
            ease: 'power2.out',
            onComplete: () => {
                el.classList.add('revealed');
            }
        });
    });

    // Property Cards Staggered Reveal
    gsap.utils.toArray('.properties-grid').forEach(grid => {
        const cards = grid.querySelectorAll('.property-card');
        if (cards.length > 0) {
            gsap.from(cards, {
                scrollTrigger: {
                    trigger: grid,
                    start: 'top 85%',
                    toggleActions: 'play none none none'
                },
                y: 60,
                opacity: 0,
                duration: 0.7,
                stagger: 0.15,
                ease: 'power2.out'
            });
        }
    });

    // Testimonial Cards with Scale
    gsap.utils.toArray('.testimonial-card').forEach((card, i) => {
        gsap.from(card, {
            scrollTrigger: {
                trigger: card,
                start: 'top 88%'
            },
            y: 40,
            opacity: 0,
            scale: 0.95,
            duration: 0.7,
            delay: i * 0.15,
            ease: 'back.out(1.3)'
        });
    });

    // Differentials with Bounce
    gsap.utils.toArray('.differential-card').forEach((card, i) => {
        gsap.from(card, {
            scrollTrigger: {
                trigger: card,
                start: 'top 88%'
            },
            y: 40,
            opacity: 0,
            scale: 0.95,
            duration: 0.7,
            delay: i * 0.12,
            ease: 'back.out(1.4)'
        });
    });

    // Timeline Items Slide In
    gsap.utils.toArray('.timeline-item').forEach((item, i) => {
        gsap.from(item, {
            scrollTrigger: {
                trigger: item,
                start: 'top 85%'
            },
            x: -30,
            opacity: 0,
            duration: 0.6,
            delay: i * 0.15,
            ease: 'power2.out'
        });
    });
}

// ── 3. Interactive Hover Micro-Animations ───────────────────────────────
function initHoverEffects() {
    document.querySelectorAll('.property-card').forEach(card => {
        card.addEventListener('mouseenter', () => {
            gsap.to(card, { y: -8, duration: 0.3, ease: 'power2.out' });
        });
        card.addEventListener('mouseleave', () => {
            gsap.to(card, { y: 0, duration: 0.3, ease: 'power2.out' });
        });
    });

    document.querySelectorAll('.glass-card').forEach(card => {
        card.addEventListener('mouseenter', () => {
            gsap.to(card, { y: -4, duration: 0.25, ease: 'power2.out' });
        });
        card.addEventListener('mouseleave', () => {
            gsap.to(card, { y: 0, duration: 0.25, ease: 'power2.out' });
        });
    });
}

// ── 4. Animated Counter for Stats ──────────────────────────────────────
function initStatCounters() {
    if (typeof ScrollTrigger === 'undefined') return;

    const statNumbers = document.querySelectorAll('.stat-number[data-count]');
    if (!statNumbers.length) return;

    statNumbers.forEach(el => {
        const target = parseInt(el.dataset.count, 10);
        if (isNaN(target)) return;

        ScrollTrigger.create({
            trigger: el,
            start: 'top 90%',
            once: true,
            onEnter: () => {
                const obj = { val: 0 };
                gsap.to(obj, {
                    val: target,
                    duration: 2,
                    ease: 'power2.out',
                    onUpdate: () => {
                        el.textContent = Math.round(obj.val).toLocaleString('pt-BR');
                    }
                });
            }
        });
    });
}

// ── 5. Header Scroll Effect ────────────────────────────────────────────
function initHeaderScroll() {
    const header = document.querySelector('.site-header');
    if (!header) return;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    }, { passive: true });
}
