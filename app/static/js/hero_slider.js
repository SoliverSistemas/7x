/* ==========================================================================
   7X Patrimonial - Hero Multi-Video Slider & Carousel Controls
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    initHeroVideoSlider();
});


/* â”€â”€ Helper: debounce para evitar centenas de chamadas no resize â”€â”€â”€ */
function debounce(fn, delay) {
    var timer;
    return function() {
        var args = arguments;
        clearTimeout(timer);
        timer = setTimeout(function() { fn.apply(this, args); }, delay || 150);
    };
}

/* â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
   loadVideoSources(videoEl)
   Popula as <source> de um vÃ­deo lazy (data-src-mp4) e dispara o download.
   Idempotente: chamaÃ§Ãµes repetidas nÃ£o refazem o trabalho.
   â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
function loadVideoSources(videoEl) {
    if (videoEl.dataset.loaded) return; // jÃ¡ iniciou o download
    videoEl.dataset.loaded = '1';

    var mp4 = videoEl.dataset.srcMp4;
    if (mp4) {
        var source = document.createElement('source');
        source.src  = mp4;
        source.type = 'video/mp4';
        videoEl.appendChild(source);
    }

    // preload="auto" faz o browser comeÃ§ar a baixar em background
    videoEl.preload = 'auto';
    videoEl.load();
}


function initHeroVideoSlider() {
    var heroSection = document.getElementById('hero-slider');
    if (!heroSection) return;

    var videos     = Array.from(heroSection.querySelectorAll('.hero-video'));
    var indicators = Array.from(heroSection.querySelectorAll('.indicator-btn'));
    var prevBtn       = document.getElementById('hero-prev-btn');
    var nextBtn       = document.getElementById('hero-next-btn');
    var playPauseBtn  = document.getElementById('hero-play-pause-btn');

    if (videos.length === 0) return;

    var currentIndex = 0;
    var isPlaying    = true;
    var SLIDE_DURATION        = 8000;
    var slideTimer            = null;
    var progressStartTime     = 0;
    var progressAnimationFrame = null;

    // ConfiguraÃ§Ã£o inicial dos vÃ­deos
    videos.forEach(function(vid, idx) {
        vid.muted       = true;
        vid.playsInline = true;
        if (idx === 0) {
            vid.classList.add('active');
            vid.play().catch(function() {});
        } else {
            vid.classList.remove('active');
            // VÃ­deos com data-src-mp4 ainda nÃ£o tÃªm source â€” aguardam o preload antecipado
            // VÃ­deos jÃ¡ com <source> (sem data-src-mp4) ficam pausados normalmente
            if (!vid.dataset.srcMp4) {
                vid.pause();
                vid.currentTime = 0;
            }
        }
    });

    /* â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
       scheduleNextPreload(activeIndex)
       Agenda o preload do prÃ³ximo vÃ­deo para iniciar a 60% do slide atual
       (= 4.8s de 8s), dando ~3s de buffer antes da transiÃ§Ã£o.
       â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
    var preloadTimer = null;
    var PRELOAD_AT   = 0.60; // dispara o preload neste % da duraÃ§Ã£o do slide

    function scheduleNextPreload(activeIndex) {
        clearTimeout(preloadTimer);
        var nextIndex = (activeIndex + 1) % videos.length;
        var nextVideo = videos[nextIndex];
        if (!nextVideo || !nextVideo.dataset.srcMp4) return; // jÃ¡ tem source ou nÃ£o Ã© lazy

        var delay = Math.floor(SLIDE_DURATION * PRELOAD_AT); // ex: 4800ms
        preloadTimer = setTimeout(function() {
            loadVideoSources(nextVideo);
        }, delay);
    }


    function updateIndicators(index) {
        indicators.forEach((ind, i) => {
            const progressBar = ind.querySelector('.indicator-progress');
            if (i === index) {
                ind.classList.add('active');
                if (progressBar) progressBar.style.width = '0%';
            } else {
                ind.classList.remove('active');
                if (progressBar) progressBar.style.width = '0%';
            }
        });
    }

    function animateProgressBar() {
        if (!isPlaying) return;

        const now = performance.now();
        const elapsed = now - progressStartTime;
        const percent = Math.min((elapsed / SLIDE_DURATION) * 100, 100);

        const activeIndicator = indicators[currentIndex];
        if (activeIndicator) {
            const progressBar = activeIndicator.querySelector('.indicator-progress');
            if (progressBar) {
                progressBar.style.width = `${percent}%`;
            }
        }

        if (elapsed < SLIDE_DURATION) {
            progressAnimationFrame = requestAnimationFrame(animateProgressBar);
        } else {
            goToSlide((currentIndex + 1) % videos.length);
        }
    }

    function startAutoSlide() {
        cancelAnimationFrame(progressAnimationFrame);
        clearTimeout(slideTimer);

        if (!isPlaying) return;

        progressStartTime = performance.now();
        progressAnimationFrame = requestAnimationFrame(animateProgressBar);

        // Agenda preload do prÃ³ximo vÃ­deo com antecipaÃ§Ã£o
        scheduleNextPreload(currentIndex);
    }

    function stopAutoSlide() {
        cancelAnimationFrame(progressAnimationFrame);
        clearTimeout(slideTimer);
    }

    function goToSlide(targetIndex) {
        if (targetIndex === currentIndex && videos[currentIndex].classList.contains('active')) return;

        var prevIndex = currentIndex;
        currentIndex  = targetIndex;

        var prevVideo = videos[prevIndex];
        var nextVideo = videos[currentIndex];

        if (prevVideo) {
            prevVideo.classList.remove('active');
            setTimeout(function() {
                if (currentIndex !== prevIndex) {
                    prevVideo.pause();
                    prevVideo.currentTime = 0;
                }
            }, 600);
        }

        if (nextVideo) {
            // Garante que o vÃ­deo tem suas sources (caso o preload antecipado
            // ainda nÃ£o tivesse disparado, ex: clique manual antecipado)
            loadVideoSources(nextVideo);
            nextVideo.classList.add('active');
            nextVideo.currentTime = 0;
            if (isPlaying) {
                nextVideo.play().catch(function() {});
            }
        }

        updateIndicators(currentIndex);

        if (isPlaying) {
            startAutoSlide(); // jÃ¡ inclui scheduleNextPreload(currentIndex)
        }
    }

    function togglePlayPause() {
        isPlaying = !isPlaying;

        const currentVideo = videos[currentIndex];
        const pauseIcon = playPauseBtn?.querySelector('.icon-pause');
        const playIcon = playPauseBtn?.querySelector('.icon-play');

        if (isPlaying) {
            if (currentVideo) currentVideo.play().catch(() => {});
            if (pauseIcon) pauseIcon.style.display = 'block';
            if (playIcon) playIcon.style.display = 'none';
            if (playPauseBtn) playPauseBtn.setAttribute('title', 'Pausar vÃ­deo');
            startAutoSlide();
        } else {
            if (currentVideo) currentVideo.pause();
            if (pauseIcon) pauseIcon.style.display = 'none';
            if (playIcon) playIcon.style.display = 'block';
            if (playPauseBtn) playPauseBtn.setAttribute('title', 'Reproduzir vÃ­deo');
            stopAutoSlide();
        }
    }

    // Event listeners
    if (nextBtn) {
        nextBtn.addEventListener('click', (e) => {
            e.preventDefault();
            goToSlide((currentIndex + 1) % videos.length);
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener('click', (e) => {
            e.preventDefault();
            goToSlide((currentIndex - 1 + videos.length) % videos.length);
        });
    }

    if (playPauseBtn) {
        playPauseBtn.addEventListener('click', (e) => {
            e.preventDefault();
            togglePlayPause();
        });
    }

    indicators.forEach((ind, i) => {
        ind.addEventListener('click', (e) => {
            e.preventDefault();
            goToSlide(i);
        });
    });

    // Start carousel
    updateIndicators(0);
    startAutoSlide();

    // Pause when tab is not visible to save resources
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            if (isPlaying && videos[currentIndex]) {
                videos[currentIndex].pause();
                stopAutoSlide();
            }
        } else {
            if (isPlaying && videos[currentIndex]) {
                videos[currentIndex].play().catch(() => {});
                startAutoSlide();
            }
        }
    });
}
