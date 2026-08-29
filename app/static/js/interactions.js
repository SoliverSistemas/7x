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
    // Efeito 3D removido para manter os cards estáticos
}

/* ══════════════════════════════════════════════════════════════════════════
   2. MAGNETIC BUTTONS — botões .btn-primary se atraem para o cursor
      Desativado em dispositivos touch (não há hover real)
   ══════════════════════════════════════════════════════════════════════════ */
function initMagneticButtons() {
    // Não aplicar em dispositivos sem hover (touch, mobile)
    if (window.matchMedia('(hover: none)').matches) return;

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


