/* ==========================================================================
   7X Patrimonial — Interactive Effects
   1. Card 3D Tilt (holographic sheen)
   2. Magnetic Buttons
   3. Custom Cursor Dot
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    initCardTilt();
    initMagneticButtons();
});

/* ══════════════════════════════════════════════════════════════════════════
   1. CARD 3D TILT — mover o mouse sobre o card inclina ele em 3D
      com reflexo de luz dourado que segue o cursor
   ══════════════════════════════════════════════════════════════════════════ */
function initCardTilt() {
    document.querySelectorAll('.property-card').forEach(card => {

        /* Injeta div de sheen (reflexo) no card */
        const sheen = document.createElement('div');
        sheen.className = 'card-sheen';
        card.appendChild(sheen);

        const MAX_TILT = 10; // graus máximos

        card.addEventListener('mousemove', e => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            /* Normalizado -1 a +1 */
            const nx = (x / rect.width  - 0.5) * 2;
            const ny = (y / rect.height - 0.5) * 2;

            const rotX = -ny * MAX_TILT;   // eixo X: inclina frente/trás
            const rotY =  nx * MAX_TILT;   // eixo Y: inclina esq/dir

            card.style.transform =
                `perspective(900px) rotateX(${rotX}deg) rotateY(${rotY}deg) translateZ(6px)`;

            /* Reflexo segue o cursor */
            sheen.style.background =
                `radial-gradient(circle at ${x}px ${y}px,
                    rgba(201,172,119,0.18) 0%,
                    rgba(201,172,119,0.06) 40%,
                    transparent 70%)`;
            sheen.style.opacity = '1';
        });

        card.addEventListener('mouseleave', () => {
            /* Retorna suavemente — transition no CSS */
            card.style.transform = '';
            sheen.style.opacity  = '0';
        });

        card.addEventListener('mousedown',  () => {
            card.style.transform = card.style.transform.replace('translateZ(6px)', 'translateZ(2px)');
        });
        card.addEventListener('mouseup',    () => {
            /* restore via mousemove ao continuar */
        });
    });
}

/* ══════════════════════════════════════════════════════════════════════════
   2. MAGNETIC BUTTONS — botões .btn-primary se atraem para o cursor
   ══════════════════════════════════════════════════════════════════════════ */
function initMagneticButtons() {
    const STRENGTH = 0.28;   // força de atração (0 = sem efeito, 1 = cursor)
    const RADIUS   = 80;     // px ao redor do botão que ativa o efeito

    document.querySelectorAll('.btn-primary, .btn-outline').forEach(btn => {
        let animId;

        btn.addEventListener('mousemove', e => {
            const rect   = btn.getBoundingClientRect();
            const cx     = rect.left + rect.width  / 2;
            const cy     = rect.top  + rect.height / 2;
            const dx     = e.clientX - cx;
            const dy     = e.clientY - cy;
            const dist   = Math.sqrt(dx * dx + dy * dy);

            if (dist < RADIUS) {
                const tx = dx * STRENGTH;
                const ty = dy * STRENGTH;
                btn.style.transform =
                    `translate(${tx}px, ${ty}px)`;
            }
        });

        btn.addEventListener('mouseleave', () => {
            /* Spring back */
            btn.style.transition = 'transform 0.5s cubic-bezier(0.34,1.56,0.64,1)';
            btn.style.transform  = 'translate(0,0)';
            setTimeout(() => { btn.style.transition = ''; }, 500);
        });
    });
}


