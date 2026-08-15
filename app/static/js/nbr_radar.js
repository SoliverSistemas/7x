/**
 * 7X Patrimonial — Radar de Bairros Nobres
 * ─────────────────────────────────────────
 * Features:
 *  • Animated polygon radar chart (Canvas) with 6 axes
 *  • Smooth polygon morphing between neighborhoods (lerp interpolation, rAF)
 *  • Concentric grid rings, axis labels, glow fills
 *  • Score counter animation with easeOutCubic
 *  • Progress bar animations for each axis KPI
 *  • Appreciation bar and profile tags updated per neighborhood
 *  • Accessible: aria-selected, role=tab/tabpanel
 */

(function () {
  'use strict';

  /* ─── NEIGHBORHOOD DATA ─────────────────────────────────────────────── */
  const AXES = ['Valorização','Liquidez','Infraestrutura','Gastronomia','Segurança','Exclusividade'];

  const NEIGHBORHOODS = {
    itaim: {
      name: 'Itaim Bibi',
      badge: 'Premium',
      desc: 'Epicentro financeiro e gastronômico de São Paulo. Alta demanda por locação corporativa e residencial. Valorização consistente e liquidez acima da média do mercado paulistano.',
      scores: [88, 95, 92, 97, 85, 88], // [Valorização, Liquidez, Infra, Gastro, Seg, Exclus]
      score7x: 92,
      price: 'R$ 22.000',
      apprec: '+67%',
      apprecPct: 67,
      tags: ['Alta Liquidez','Corporativo','Luxo Urbano','Gastronomia Top','FIPE+'],
    },
    jardins: {
      name: 'Jardins',
      badge: 'Ultra Luxo',
      desc: 'O bairro mais exclusivo de São Paulo. Endereço icônico, boutiques internacionais e residências de alto padrão que raramente chegam ao mercado. Demanda sempre supera a oferta.',
      scores: [82, 78, 96, 99, 92, 99],
      score7x: 96,
      price: 'R$ 25.000',
      apprec: '+58%',
      apprecPct: 58,
      tags: ['Ultra Exclusivo','Moda & Cultura','Raridade de Oferta','Turismo de Luxo','Status'],
    },
    moema: {
      name: 'Moema',
      badge: 'Residencial',
      desc: 'Perfil residencial familiar e verde. Parques, restaurantes premiados e escolas de elite. Excelente custo-benefício em relação aos vizinhos premium com valorização acelerada.',
      scores: [79, 82, 88, 88, 89, 75],
      score7x: 84,
      price: 'R$ 18.000',
      apprec: '+71%',
      apprecPct: 71,
      tags: ['Familiar','Parques','Escolas Elite','Custo-Benefício','Verde Urbano'],
    },
    pinheiros: {
      name: 'Pinheiros',
      badge: 'Cultural',
      desc: 'Bairro vibrante e criativo com ascensão rápida de valor. Público jovem de alta renda, cultural e sofisticado. Forte demanda por locação de curta e longa duração.',
      scores: [85, 88, 85, 93, 76, 72],
      score7x: 83,
      price: 'R$ 16.000',
      apprec: '+82%',
      apprecPct: 82,
      tags: ['Cultural','Jovem & Criativo','Valorização Rápida','Gastronomia Cult','Bike-Friendly'],
    },
    altopinheiros: {
      name: 'Alto de Pinheiros',
      badge: 'Residencial Nobre',
      desc: 'Tranquilidade e privacidade em casas grandes e arborizado. Distante do tráfego intenso, com ruas largas e vizinhança discreta. Perfil de família que valoriza silêncio e espaço.',
      scores: [75, 70, 80, 70, 94, 88],
      score7x: 80,
      price: 'R$ 20.000',
      apprec: '+55%',
      apprecPct: 55,
      tags: ['Privacidade','Casas Grandes','Arborizado','Silencioso','Família'],
    },
    vnc: {
      name: 'Vila Nova Conceição',
      badge: 'Escasso & Nobre',
      desc: 'O bairro com menor oferta de imóveis nobres em SP. Adjacente ao Ibirapuera e ao Itaim, concentra embaixadores, executivos e celebrities em muros altos e ruas sem saída.',
      scores: [90, 68, 88, 85, 96, 97],
      score7x: 94,
      price: 'R$ 24.000',
      apprec: '+63%',
      apprecPct: 63,
      tags: ['Máxima Discrição','Ibirapuera','Raridade Absoluta','VIP','Embassy Row'],
    },
    morumbi: {
      name: 'Morumbi',
      badge: 'Mansões',
      desc: 'Terrenos amplos, mansões e condomínios fechados com segurança máxima. Endereço histórico da elite paulistana. Valorização estável e demanda por locação de alto ticket.',
      scores: [72, 65, 78, 65, 97, 85],
      score7x: 78,
      price: 'R$ 15.000',
      apprec: '+48%',
      apprecPct: 48,
      tags: ['Condomínios Fechados','Mansões','Segurança Máxima','Terrenos Amplos','Privê'],
    },
  };

  /* ─── THEME COLORS ───────────────────────────────────────────────────── */
  function getCSSVar(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }

  /* ─── STATE ──────────────────────────────────────────────────────────── */
  let current = 'itaim';
  let target  = 'itaim';
  let animProgress = 1; // 0→1 morph
  let animRAF = null;
  let fromScores = [...NEIGHBORHOODS['itaim'].scores];
  let toScores   = [...NEIGHBORHOODS['itaim'].scores];
  let fromScore7x = NEIGHBORHOODS['itaim'].score7x;
  let toScore7x   = NEIGHBORHOODS['itaim'].score7x;

  /* ─── CANVAS SETUP ───────────────────────────────────────────────────── */
  const canvas = document.getElementById('nbr-radar-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  function resizeCanvas() {
    const wrap = canvas.parentElement;
    const size = Math.min(wrap.clientWidth, wrap.clientHeight) - 64;
    const dpr = window.devicePixelRatio || 1;
    canvas.width  = size * dpr;
    canvas.height = size * dpr;
    canvas.style.width  = size + 'px';
    canvas.style.height = size + 'px';
    ctx.scale(dpr, dpr);
    drawRadar(lerpScores(fromScores, toScores, 1));
  }

  /* ─── MATH HELPERS ───────────────────────────────────────────────────── */
  function lerp(a, b, t) { return a + (b - a) * t; }
  function easeInOut(t)  { return t < 0.5 ? 2*t*t : -1+(4-2*t)*t; }
  function easeOut(t)    { return 1 - Math.pow(1 - t, 3); }

  function lerpScores(a, b, t) {
    return a.map((v, i) => lerp(v, b[i], easeInOut(t)));
  }

  function radarPoint(cx, cy, r, angleOffset, index, count, value) {
    const angle = angleOffset + (index / count) * Math.PI * 2 - Math.PI / 2;
    return {
      x: cx + r * (value / 100) * Math.cos(angle),
      y: cy + r * (value / 100) * Math.sin(angle),
    };
  }

  /* ─── DRAW ───────────────────────────────────────────────────────────── */
  function drawRadar(scores) {
    const W = canvas.width  / (window.devicePixelRatio || 1);
    const H = canvas.height / (window.devicePixelRatio || 1);
    const cx = W / 2;
    const cy = H / 2;
    const R  = Math.min(W, H) / 2 - 32;
    const N  = AXES.length;
    const ANGLE_OFFSET = 0;
    const RINGS = 5;

    ctx.clearRect(0, 0, W, H);

    const gold = '#c9ac77';
    const goldLight = '#f0d98a';
    const muted = 'rgba(107,101,96,0.5)';
    const gridColor = 'rgba(201,172,119,0.08)';
    const axisColor = 'rgba(201,172,119,0.15)';

    /* -- Grid rings -- */
    for (let ring = 1; ring <= RINGS; ring++) {
      const r = (ring / RINGS) * R;
      ctx.beginPath();
      for (let i = 0; i < N; i++) {
        const angle = ANGLE_OFFSET + (i / N) * Math.PI * 2 - Math.PI / 2;
        const x = cx + r * Math.cos(angle);
        const y = cy + r * Math.sin(angle);
        i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
      }
      ctx.closePath();
      ctx.strokeStyle = gridColor;
      ctx.lineWidth = ring === RINGS ? 1.5 : 1;
      ctx.stroke();

      /* Ring label at top */
      if (ring % 2 === 0) {
        const labelAngle = -Math.PI / 2;
        const lx = cx + r * Math.cos(labelAngle);
        const ly = cy + r * Math.sin(labelAngle);
        ctx.font = '9px Inter, sans-serif';
        ctx.fillStyle = 'rgba(107,101,96,0.6)';
        ctx.textAlign = 'center';
        ctx.fillText(`${ring * 20}`, lx, ly - 4);
      }
    }

    /* -- Axis lines & labels -- */
    for (let i = 0; i < N; i++) {
      const angle = ANGLE_OFFSET + (i / N) * Math.PI * 2 - Math.PI / 2;
      const ex = cx + R * Math.cos(angle);
      const ey = cy + R * Math.sin(angle);

      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(ex, ey);
      ctx.strokeStyle = axisColor;
      ctx.lineWidth = 1;
      ctx.stroke();

      /* Axis label */
      const lpad = 14;
      const lx = cx + (R + lpad) * Math.cos(angle);
      const ly = cy + (R + lpad) * Math.sin(angle);

      ctx.font = 'bold 10px Inter, sans-serif';
      ctx.fillStyle = 'rgba(196,186,168,0.85)';
      ctx.textAlign = Math.abs(Math.cos(angle)) < 0.1 ? 'center'
                    : Math.cos(angle) > 0 ? 'left' : 'right';
      ctx.textBaseline = Math.sin(angle) < -0.5 ? 'bottom'
                       : Math.sin(angle) > 0.5 ? 'top' : 'middle';
      ctx.fillText(AXES[i], lx, ly);
    }

    /* -- Glow fill polygon -- */
    const pts = scores.map((v, i) => radarPoint(cx, cy, R, ANGLE_OFFSET, i, N, v));

    ctx.beginPath();
    pts.forEach((p, i) => i === 0 ? ctx.moveTo(p.x, p.y) : ctx.lineTo(p.x, p.y));
    ctx.closePath();

    const grad = ctx.createRadialGradient(cx, cy, 0, cx, cy, R);
    grad.addColorStop(0,   'rgba(201,172,119,0.35)');
    grad.addColorStop(0.7, 'rgba(201,172,119,0.18)');
    grad.addColorStop(1,   'rgba(201,172,119,0.05)');
    ctx.fillStyle = grad;
    ctx.fill();

    /* Stroke */
    ctx.beginPath();
    pts.forEach((p, i) => i === 0 ? ctx.moveTo(p.x, p.y) : ctx.lineTo(p.x, p.y));
    ctx.closePath();
    ctx.strokeStyle = gold;
    ctx.lineWidth = 2.5;
    ctx.shadowColor = gold;
    ctx.shadowBlur = 10;
    ctx.stroke();
    ctx.shadowBlur = 0;

    /* Vertex dots */
    pts.forEach(p => {
      ctx.beginPath();
      ctx.arc(p.x, p.y, 4, 0, Math.PI * 2);
      ctx.fillStyle = gold;
      ctx.strokeStyle = 'var(--bg-card, #131618)';
      ctx.lineWidth = 2;
      ctx.fill();
      ctx.stroke();

      /* glow dot */
      ctx.beginPath();
      ctx.arc(p.x, p.y, 7, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(201,172,119,0.15)';
      ctx.fill();
    });
  }

  /* ─── ANIMATION LOOP ─────────────────────────────────────────────────── */
  const ANIM_DUR = 500; // ms
  let animStart = null;

  function animateMorph(ts) {
    if (!animStart) animStart = ts;
    const elapsed = ts - animStart;
    animProgress = Math.min(elapsed / ANIM_DUR, 1);

    const interpolated = lerpScores(fromScores, toScores, animProgress);
    drawRadar(interpolated);

    /* Score counter */
    const scoreEl = document.getElementById('nbr-score-number');
    if (scoreEl) {
      scoreEl.textContent = Math.round(lerp(fromScore7x, toScore7x, easeOut(animProgress)));
    }

    if (animProgress < 1) {
      animRAF = requestAnimationFrame(animateMorph);
    } else {
      fromScores  = [...toScores];
      fromScore7x = toScore7x;
      updateDetail(target);
    }
  }

  function startMorph(key) {
    if (animRAF) cancelAnimationFrame(animRAF);
    animStart    = null;
    fromScores   = lerpScores(fromScores, toScores, animProgress);
    fromScore7x  = lerp(fromScore7x, toScore7x, animProgress);
    toScores     = [...NEIGHBORHOODS[key].scores];
    toScore7x    = NEIGHBORHOODS[key].score7x;
    current      = key;
    animRAF      = requestAnimationFrame(animateMorph);
  }

  /* ─── DETAIL PANEL UPDATE ────────────────────────────────────────────── */
  function updateDetail(key) {
    const nbr = NEIGHBORHOODS[key];

    const setTxt = (id, v) => { const el = document.getElementById(id); if (el) el.textContent = v; };
    setTxt('nbr-detail-name', nbr.name);
    setTxt('nbr-detail-badge', nbr.badge);
    setTxt('nbr-detail-desc', nbr.desc);
    setTxt('nbr-radar-name', nbr.name);
    setTxt('nbr-price-val', nbr.price);
    setTxt('nbr-apprec-val', nbr.apprec);

    const apprecBar = document.getElementById('nbr-apprec-bar');
    if (apprecBar) apprecBar.style.width = Math.min(nbr.apprecPct, 100) + '%';

    /* Axis KPIs */
    const axisGrid = document.getElementById('nbr-axis-grid');
    if (axisGrid) {
      axisGrid.innerHTML = AXES.map((axis, i) => `
        <div class="nbr-axis-item">
          <span class="nbr-axis-name">${axis}</span>
          <div class="nbr-axis-bar-track">
            <div class="nbr-axis-bar-fill" style="width:0" data-target="${nbr.scores[i]}"></div>
          </div>
          <span class="nbr-axis-score">${nbr.scores[i]}/100</span>
        </div>
      `).join('');

      /* Animate bars */
      requestAnimationFrame(() => {
        axisGrid.querySelectorAll('.nbr-axis-bar-fill').forEach(bar => {
          const t = parseInt(bar.dataset.target, 10);
          bar.style.width = t + '%';
        });
      });
    }

    /* Profile tags */
    const tagsEl = document.getElementById('nbr-profile-tags');
    if (tagsEl) {
      tagsEl.innerHTML = nbr.tags.map(t => `<span class="nbr-tag">${t}</span>`).join('');
    }

    /* CTA link */
    const ctaBtn = document.getElementById('nbr-cta-btn');
    if (ctaBtn) {
      const q = encodeURIComponent(nbr.name.split(' ')[0]);
      ctaBtn.href = ctaBtn.href.split('?')[0] + '?q=' + q;
    }

    /* Flip detail card briefly */
    const card = document.getElementById('nbr-detail-card');
    if (card) {
      card.classList.add('switching');
      setTimeout(() => card.classList.remove('switching'), 180);
    }
  }

  /* ─── PILL INTERACTION ───────────────────────────────────────────────── */
  function selectNeighborhood(key) {
    if (key === current && animProgress >= 1) return;
    target = key;

    document.querySelectorAll('.nbr-pill').forEach(p => {
      const active = p.dataset.nbr === key;
      p.classList.toggle('active', active);
      p.setAttribute('aria-selected', active);
    });

    const panelEl = document.getElementById('nbr-panel');
    if (panelEl) panelEl.setAttribute('aria-labelledby', 'tab-' + key);

    startMorph(key);
  }

  document.querySelectorAll('.nbr-pill').forEach(pill => {
    pill.addEventListener('click', () => selectNeighborhood(pill.dataset.nbr));
  });

  /* ─── INIT ───────────────────────────────────────────────────────────── */
  window.addEventListener('resize', () => {
    resizeCanvas();
  });

  // Observe visibility — run initial animation only when section enters viewport
  const section = document.getElementById('nbr-section');
  if (section) {
    const io = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting) {
        resizeCanvas();
        updateDetail('itaim');
        io.disconnect();
      }
    }, { threshold: 0.15 });
    io.observe(section);
  } else {
    resizeCanvas();
    updateDetail('itaim');
  }

})();
