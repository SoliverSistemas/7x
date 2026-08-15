# Backup: Moodboard Matcher (7X Lifestyle DNA)

## HTML
`html
<!-- ══ 7X Lifestyle DNA ════════════════════════════════════════════ -->
<section class="section dna-section" id="dna-section">
    <div class="container">

        <div class="dna-header reveal">
            <div class="section-eyebrow">
                <span class="eyebrow-line"></span>
                <span>CURADORIA VISUAL POR IA</span>
            </div>
            <h2 class="dna-title">Descubra seu<br><span class="dna-title-gold">DNA Imobiliário</span></h2>
            <p class="dna-subtitle">Não busque por "quartos e vagas". Escolha até 3 imagens que representam sua estética de vida e deixe nosso algoritmo encontrar a atmosfera perfeita para você.</p>
        </div>

        <!-- Interface de Seleção -->
        <div class="dna-interface" id="dna-interface">
            
            <div class="dna-grid">
                <!-- Card 1: Minimalista / Moderno -->
                <button class="dna-card" data-trait="minimalista" aria-pressed="false">
                    <div class="dna-img-wrap">
                        <img src="https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=600&q=80" alt="Arquitetura Minimalista" loading="lazy">
                    </div>
                    <div class="dna-card-overlay">
                        <span class="dna-card-label">Arquitetura Pura</span>
                        <div class="dna-check">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
                        </div>
                    </div>
                </button>

                <!-- Card 2: Natureza / Refúgio -->
                <button class="dna-card" data-trait="natureza" aria-pressed="false">
                    <div class="dna-img-wrap">
                        <img src="https://images.unsplash.com/photo-1511884642898-4c92249e20b6?auto=format&fit=crop&w=600&q=80" alt="Refúgio Natural" loading="lazy">
                    </div>
                    <div class="dna-card-overlay">
                        <span class="dna-card-label">Refúgio Verde</span>
                        <div class="dna-check">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
                        </div>
                    </div>
                </button>

                <!-- Card 3: Clássico / Arte -->
                <button class="dna-card" data-trait="classico" aria-pressed="false">
                    <div class="dna-img-wrap">
                        <img src="https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=600&q=80" alt="Design Clássico" loading="lazy">
                    </div>
                    <div class="dna-card-overlay">
                        <span class="dna-card-label">Design &amp; Arte</span>
                        <div class="dna-check">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
                        </div>
                    </div>
                </button>

                <!-- Card 4: Vista / Urbano -->
                <button class="dna-card" data-trait="urbano" aria-pressed="false">
                    <div class="dna-img-wrap">
                        <img src="https://images.unsplash.com/photo-1449844908441-8829872d2607?auto=format&fit=crop&w=600&q=80" alt="Vista Panorâmica" loading="lazy">
                    </div>
                    <div class="dna-card-overlay">
                        <span class="dna-card-label">Vista Panorâmica</span>
                        <div class="dna-check">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
                        </div>
                    </div>
                </button>
                
                <!-- Card 5: Privacidade / Exclusivo -->
                <button class="dna-card" data-trait="exclusivo" aria-pressed="false">
                    <div class="dna-img-wrap">
                        <img src="https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=600&q=80" alt="Privacidade Absoluta" loading="lazy">
                    </div>
                    <div class="dna-card-overlay">
                        <span class="dna-card-label">Privacidade Absoluta</span>
                        <div class="dna-check">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
                        </div>
                    </div>
                </button>

                <!-- Card 6: Entretenimento / Social -->
                <button class="dna-card" data-trait="social" aria-pressed="false">
                    <div class="dna-img-wrap">
                        <img src="https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?auto=format&fit=crop&w=600&q=80" alt="Vida Social" loading="lazy">
                    </div>
                    <div class="dna-card-overlay">
                        <span class="dna-card-label">Entretenimento</span>
                        <div class="dna-check">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
                        </div>
                    </div>
                </button>
            </div>

            <div class="dna-footer">
                <div class="dna-counter">Selecionadas: <span id="dna-count">0</span>/3</div>
                <button class="btn btn-primary dna-btn" id="dna-analyze-btn" disabled>
                    <svg class="dna-sparkle" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>
                    Gerar Análise de Perfil
                </button>
            </div>
            
            <!-- Loading overlay -->
            <div class="dna-loading" id="dna-loading">
                <div class="dna-spinner"></div>
                <p class="dna-loading-text">Processando assinaturas visuais...</p>
                <div class="dna-loading-progress">
                    <div class="dna-loading-bar" id="dna-loading-bar"></div>
                </div>
            </div>
        </div>

        <!-- Resultado da Análise -->
        <div class="dna-result" id="dna-result">
            <div class="dna-result-header">
                <span class="badge badge-gold">SEU DNA IMOBILIÁRIO</span>
                <h3 class="dna-profile-title" id="dna-profile-title">Urbano Minimalista</h3>
            </div>
            
            <div class="dna-result-body">
                <div class="dna-result-text">
                    <p id="dna-profile-desc">Sua assinatura estética exige linhas retas, ausência de excessos e integração visual com a metrópole. O concreto aparente, vidro do chão ao teto e automação invisível são fundamentais para o seu bem-estar.</p>
                    
                    <div class="dna-match-locations">
                        <span class="dna-match-label">BAIRROS COMPATÍVEIS:</span>
                        <div class="dna-tags" id="dna-match-tags">
                            <span class="dna-tag">Itaim Bibi</span>
                            <span class="dna-tag">Vila Olímpia</span>
                        </div>
                    </div>
                </div>
                
                <div class="dna-result-cta">
                    <div class="dna-match-score">
                        <svg viewBox="0 0 36 36" class="dna-score-chart">
                            <path class="dna-score-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                            <path class="dna-score-fill" id="dna-score-fill" stroke-dasharray="98, 100" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                        </svg>
                        <div class="dna-score-num">98%<br><span>Match</span></div>
                    </div>
                    <a href="{{ url_for('properties.list_properties') }}" class="btn btn-outline dna-result-btn" id="dna-result-btn">
                        Ver Coleção Recomendada
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
                    </a>
                    <button class="dna-reset-btn" id="dna-reset-btn">Refazer Análise</button>
                </div>
            </div>
        </div>

    </div><!-- /.container -->
</section>




`

## CSS
`css
/* ══════════════════════════════════════════════════════════════════════════
   7X LIFESTYLE DNA (MOODBOARD MATCHER)
   ══════════════════════════════════════════════════════════════════════════ */

.dna-section {
    background: var(--bg-main);
    padding: 7rem 0;
    position: relative;
    overflow: hidden;
}

/* ── Header ─────────────────────────────────────────────────────────────── */
.dna-header {
    text-align: center;
    max-width: 640px;
    margin: 0 auto 4rem;
}

.dna-title {
    font-size: clamp(2rem, 4vw, 3.2rem);
    font-weight: 800;
    line-height: 1.15;
    color: var(--text-primary);
    margin-top: 0.75rem;
    letter-spacing: -0.03em;
}

.dna-title-gold {
    background: linear-gradient(105deg, var(--primary-hover) 0%, #f0d98a 40%, var(--primary) 70%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 4s linear infinite;
}

.dna-subtitle {
    font-size: 1.05rem;
    color: var(--text-secondary);
    margin-top: 1rem;
    line-height: 1.7;
}

/* ── Interface ──────────────────────────────────────────────────────────── */
.dna-interface {
    max-width: 900px;
    margin: 0 auto;
    position: relative;
    transition: opacity 0.4s ease;
}

.dna-interface.analyzing {
    opacity: 0.5;
    pointer-events: none;
}

.dna-interface.hidden {
    display: none;
}

/* ── Grid ───────────────────────────────────────────────────────────────── */
.dna-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
    margin-bottom: 3rem;
}

/* ── Cards ──────────────────────────────────────────────────────────────── */
.dna-card {
    position: relative;
    border: none;
    background: transparent;
    padding: 0;
    border-radius: 16px;
    overflow: hidden;
    cursor: pointer;
    aspect-ratio: 4/5;
    transition: transform 0.3s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.3s ease;
}

.dna-card::after {
    content: '';
    position: absolute;
    inset: 0;
    border: 2px solid transparent;
    border-radius: 16px;
    transition: border-color 0.3s ease;
    z-index: 10;
    pointer-events: none;
}

.dna-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 30px rgba(0,0,0,0.4);
}

.dna-img-wrap {
    position: absolute;
    inset: 0;
    overflow: hidden;
}

.dna-img-wrap img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.6s ease, filter 0.4s ease;
    filter: brightness(0.7) contrast(1.1);
}

.dna-card:hover .dna-img-wrap img {
    transform: scale(1.05);
    filter: brightness(0.9) contrast(1.1);
}

.dna-card-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(to top, rgba(11,15,25,0.9) 0%, rgba(11,15,25,0.2) 50%, transparent 100%);
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    padding: 1.5rem;
    z-index: 2;
}

.dna-card-label {
    color: #fff;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    transform: translateY(10px);
    opacity: 0.9;
    transition: all 0.3s ease;
    text-align: left;
}

.dna-card:hover .dna-card-label {
    transform: translateY(0);
    opacity: 1;
}

.dna-check {
    position: absolute;
    top: 1.25rem;
    right: 1.25rem;
    width: 28px;
    height: 28px;
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: transparent;
    transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
    transform: scale(0.8);
    opacity: 0;
}

/* Selected State */
.dna-card[aria-pressed="true"] {
    transform: scale(0.96);
    box-shadow: 0 0 0 4px rgba(201,172,119,0.3);
}

.dna-card[aria-pressed="true"]::after {
    border-color: var(--primary);
}

.dna-card[aria-pressed="true"] .dna-img-wrap img {
    filter: brightness(0.5) sepia(0.3) hue-rotate(5deg);
    transform: scale(1);
}

.dna-card[aria-pressed="true"] .dna-check {
    opacity: 1;
    transform: scale(1);
    background: var(--primary);
    border-color: var(--primary);
    color: #0d1012;
}

.dna-card[aria-pressed="true"] .dna-card-label {
    color: var(--primary);
}

/* ── Footer / Controls ──────────────────────────────────────────────────── */
.dna-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.5rem 2rem;
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.dna-counter {
    font-size: 0.9rem;
    color: var(--text-secondary);
    font-weight: 600;
}

#dna-count {
    color: var(--text-primary);
    font-size: 1.1rem;
}

.dna-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.8rem 1.5rem;
    font-size: 0.95rem;
    transition: all 0.3s ease;
}

.dna-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
    background: var(--bg-surface);
    color: var(--text-muted);
    border-color: var(--border-color);
}

.dna-sparkle {
    transition: transform 0.3s ease;
}

.dna-btn:not(:disabled):hover .dna-sparkle {
    transform: rotate(15deg) scale(1.1);
}

/* ── Loading Overlay ────────────────────────────────────────────────────── */
.dna-loading {
    position: absolute;
    inset: 0;
    background: rgba(11,15,25,0.85);
    backdrop-filter: blur(12px);
    z-index: 20;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-radius: 20px;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.4s ease;
}

.dna-loading.active {
    opacity: 1;
    pointer-events: auto;
}

.dna-spinner {
    width: 48px;
    height: 48px;
    border: 3px solid rgba(201,172,119,0.2);
    border-top-color: var(--primary);
    border-radius: 50%;
    animation: dna-spin 1s linear infinite;
    margin-bottom: 1.5rem;
}

@keyframes dna-spin {
    to { transform: rotate(360deg); }
}

.dna-loading-text {
    font-size: 1.1rem;
    color: var(--primary);
    font-weight: 600;
    letter-spacing: 0.05em;
    margin-bottom: 1rem;
}

.dna-loading-progress {
    width: 200px;
    height: 4px;
    background: rgba(255,255,255,0.1);
    border-radius: 2px;
    overflow: hidden;
}

.dna-loading-bar {
    height: 100%;
    width: 0%;
    background: var(--primary);
    transition: width 0.3s ease;
}

/* ── Result ─────────────────────────────────────────────────────────────── */
.dna-result {
    max-width: 800px;
    margin: 0 auto;
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 24px;
    padding: 3rem;
    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    display: none;
    opacity: 0;
    transform: translateY(20px);
    animation: slideUpFade 0.6s ease forwards;
}

.dna-result.active {
    display: block;
}

@keyframes slideUpFade {
    to { opacity: 1; transform: translateY(0); }
}

.dna-result-header {
    text-align: center;
    margin-bottom: 2.5rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

.dna-profile-title {
    font-size: 2.4rem;
    font-weight: 800;
    color: var(--text-primary);
    margin-top: 1rem;
    letter-spacing: -0.02em;
}

.dna-result-body {
    display: grid;
    grid-template-columns: 1fr 280px;
    gap: 3rem;
}

.dna-result-text p {
    font-size: 1.05rem;
    color: var(--text-secondary);
    line-height: 1.8;
    margin-bottom: 2rem;
}

.dna-match-label {
    font-size: 0.7rem;
    font-weight: 700;
    color: var(--text-muted);
    letter-spacing: 0.1em;
    display: block;
    margin-bottom: 1rem;
}

.dna-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
}

.dna-tag {
    background: rgba(201,172,119,0.08);
    border: 1px solid rgba(201,172,119,0.2);
    color: var(--primary);
    padding: 0.4rem 1rem;
    border-radius: var(--radius-full);
    font-size: 0.85rem;
    font-weight: 600;
}

.dna-result-cta {
    display: flex;
    flex-direction: column;
    align-items: center;
    background: rgba(0,0,0,0.2);
    padding: 2rem;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.05);
}

.dna-match-score {
    position: relative;
    width: 120px;
    height: 120px;
    margin-bottom: 1.5rem;
}

.dna-score-chart {
    width: 100%;
    height: 100%;
    transform: rotate(-90deg);
}

.dna-score-bg {
    fill: none;
    stroke: rgba(255,255,255,0.05);
    stroke-width: 2.5;
}

.dna-score-fill {
    fill: none;
    stroke: var(--primary);
    stroke-width: 2.5;
    stroke-linecap: round;
    transition: stroke-dasharray 1.5s ease-out;
}

.dna-score-num {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: 1.8rem;
    font-weight: 800;
    color: var(--text-primary);
    line-height: 1;
}

.dna-score-num span {
    font-size: 0.7rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
    margin-top: 0.2rem;
}

.dna-result-btn {
    width: 100%;
    justify-content: center;
    margin-bottom: 1rem;
}

.dna-reset-btn {
    background: transparent;
    border: none;
    color: var(--text-muted);
    font-size: 0.8rem;
    text-decoration: underline;
    cursor: pointer;
    transition: color 0.2s ease;
}

.dna-reset-btn:hover {
    color: var(--text-primary);
}

/* ── Responsive ─────────────────────────────────────────────────────────── */
@media (max-width: 900px) {
    .dna-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    .dna-result-body {
        grid-template-columns: 1fr;
        gap: 2rem;
    }
}

@media (max-width: 600px) {
    .dna-grid {
        grid-template-columns: 1fr;
    }
    .dna-footer {
        flex-direction: column;
        gap: 1rem;
        text-align: center;
    }
    .dna-btn {
        width: 100%;
        justify-content: center;
    }
    .dna-result {
        padding: 2rem 1.5rem;
    }
}


`

## JS
`javascript
﻿/**
 * 7X — DNA Imobiliário (Moodboard Matcher)
 */

(function () {
  'use strict';

  const MAX_SELECTIONS = 3;
  let selectedTraits = [];

  const PROFILES = [
    {
      traits: ['minimalista', 'urbano', 'classico'],
      title: 'Urbano Minimalista',
      desc: 'Sua assinatura estética exige linhas retas, ausência de excessos e integração visual com a metrópole. O concreto aparente, vidro do chão ao teto e automação invisível são fundamentais para o seu bem-estar.',
      locations: ['Itaim Bibi', 'Vila Olímpia', 'Pinheiros']
    },
    {
      traits: ['natureza', 'exclusivo', 'classico'],
      title: 'Refúgio Clássico',
      desc: 'Você busca um verdadeiro oásis na cidade. Ambientes amplos, madeiras nobres, jardins privativos e absoluto silêncio. Um estilo de vida onde o luxo é medido pelo espaço e pela privacidade.',
      locations: ['Alto de Pinheiros', 'Jardim Europa', 'Morumbi']
    },
    {
      traits: ['social', 'urbano', 'minimalista'],
      title: 'Social High-Tech',
      desc: 'Sua casa é o palco. Coberturas duplex, varandas gourmet integradas, adegas climatizadas e uma vista espetacular para receber convidados. O pulso da cidade é o seu cenário.',
      locations: ['Vila Nova Conceição', 'Jardins', 'Itaim Bibi']
    },
    {
      traits: ['natureza', 'social', 'exclusivo'],
      title: 'Resort Privativo',
      desc: 'Para você, o imóvel ideal deve ter a infraestrutura de um hotel 6 estrelas. Spas privativos, academias de ponta, segurança máxima e áreas sociais que parecem extensões de clubes exclusivos.',
      locations: ['Fazenda Boa Vista', 'Cidade Jardim', 'Alphaville']
    }
  ];

  const cards = document.querySelectorAll('.dna-card');
  const countEl = document.getElementById('dna-count');
  const btnAnalyze = document.getElementById('dna-analyze-btn');

  const interfaceEl = document.getElementById('dna-interface');
  const loadingEl = document.getElementById('dna-loading');
  const loadingBar = document.getElementById('dna-loading-bar');
  const resultEl = document.getElementById('dna-result');

  if (!cards.length) return;

  /* Card Click Handler */
  cards.forEach(card => {
    card.addEventListener('click', () => {
      const trait = card.dataset.trait;
      const isSelected = card.getAttribute('aria-pressed') === 'true';

      if (isSelected) {
        // Unselect
        card.setAttribute('aria-pressed', 'false');
        selectedTraits = selectedTraits.filter(t => t !== trait);
      } else {
        // Select (if under limit)
        if (selectedTraits.length < MAX_SELECTIONS) {
          card.setAttribute('aria-pressed', 'true');
          selectedTraits.push(trait);
        } else {
          // Visual feedback if limit reached
          card.style.transform = 'translateX(5px)';
          setTimeout(() => card.style.transform = 'translateX(-5px)', 50);
          setTimeout(() => card.style.transform = 'translateX(5px)', 100);
          setTimeout(() => card.style.transform = 'translateX(0)', 150);
        }
      }

      // Update UI
      countEl.textContent = selectedTraits.length;
      btnAnalyze.disabled = selectedTraits.length === 0;
      
      if (selectedTraits.length === MAX_SELECTIONS) {
        btnAnalyze.style.animation = 'ring-pulse 1.5s ease-out infinite';
        btnAnalyze.style.boxShadow = '0 0 20px rgba(201,172,119,0.4)';
      } else {
        btnAnalyze.style.animation = 'none';
        btnAnalyze.style.boxShadow = 'none';
      }
    });
  });

  /* Analyze Logic */
  btnAnalyze.addEventListener('click', () => {
    // 1. Show loading state
    interfaceEl.classList.add('analyzing');
    loadingEl.classList.add('active');
    
    // Simulate complex progress
    let progress = 0;
    const interval = setInterval(() => {
      progress += Math.random() * 15;
      if (progress > 100) progress = 100;
      loadingBar.style.width = progress + '%';
      
      if (progress === 100) {
        clearInterval(interval);
        setTimeout(showResult, 600); // slight pause at 100%
      }
    }, 200);
  });

  function showResult() {
    // Determine profile
    let bestMatch = PROFILES[0];
    let maxScore = -1;

    PROFILES.forEach(profile => {
      let score = 0;
      profile.traits.forEach(t => {
        if (selectedTraits.includes(t)) score++;
      });
      if (score > maxScore) {
        maxScore = score;
        bestMatch = profile;
      }
    });

    // Populate result
    document.getElementById('dna-profile-title').textContent = bestMatch.title;
    document.getElementById('dna-profile-desc').textContent = bestMatch.desc;
    
    const tagsContainer = document.getElementById('dna-match-tags');
    tagsContainer.innerHTML = '';
    bestMatch.locations.forEach(loc => {
      const span = document.createElement('span');
      span.className = 'dna-tag';
      span.textContent = loc;
      tagsContainer.appendChild(span);
    });

    // Generate random high score based on match
    const baseScore = maxScore === 3 ? 98 : (maxScore === 2 ? 89 : 76);
    const finalScore = baseScore + Math.floor(Math.random() * 2);

    // Switch views
    interfaceEl.classList.add('hidden');
    interfaceEl.classList.remove('analyzing');
    loadingEl.classList.remove('active');
    loadingBar.style.width = '0%';
    
    resultEl.classList.add('active');

    // Animate stroke
    setTimeout(() => {
      document.getElementById('dna-score-fill').style.strokeDasharray = `${finalScore}, 100`;
      
      // Update number
      const numEl = document.querySelector('.dna-score-num');
      let start = 0;
      const countInt = setInterval(() => {
        start += 2;
        if (start >= finalScore) {
          start = finalScore;
          clearInterval(countInt);
        }
        numEl.innerHTML = `${start}%<br><span>Match</span>`;
      }, 20);
    }, 300);
  }

  /* Reset Logic */
  document.getElementById('dna-reset-btn').addEventListener('click', () => {
    resultEl.classList.remove('active');
    interfaceEl.classList.remove('hidden');
    
    // Reset cards
    cards.forEach(card => card.setAttribute('aria-pressed', 'false'));
    selectedTraits = [];
    countEl.textContent = '0';
    btnAnalyze.disabled = true;
    document.getElementById('dna-score-fill').style.strokeDasharray = `0, 100`;
    
    btnAnalyze.style.animation = 'none';
    btnAnalyze.style.boxShadow = 'none';
    
    // Scroll back to section top
    document.getElementById('dna-section').scrollIntoView({ behavior: 'smooth' });
  });

})();

`
