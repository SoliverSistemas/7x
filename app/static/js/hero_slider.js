/* ==========================================================================
   7X Patrimonial - Hero Multi-Video Slider & Carousel Controls
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    initHeroVideoSlider();
    initStickySearchBar();
});

function initHeroVideoSlider() {
    const heroSection = document.getElementById('hero-slider');
    if (!heroSection) return;

    const videos = Array.from(heroSection.querySelectorAll('.hero-video'));
    const indicators = Array.from(heroSection.querySelectorAll('.indicator-btn'));
    const prevBtn = document.getElementById('hero-prev-btn');
    const nextBtn = document.getElementById('hero-next-btn');
    const playPauseBtn = document.getElementById('hero-play-pause-btn');

    if (videos.length === 0) return;

    let currentIndex = 0;
    let isPlaying = true;
    const SLIDE_DURATION = 8000; // 8 seconds per video
    let slideTimer = null;
    let progressStartTime = 0;
    let progressAnimationFrame = null;

    // Set initial video playback
    videos.forEach((vid, idx) => {
        vid.muted = true;
        vid.playsInline = true;
        if (idx === 0) {
            vid.classList.add('active');
            vid.play().catch(() => {});
        } else {
            vid.classList.remove('active');
            vid.pause();
            vid.currentTime = 0;
        }
    });

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
    }

    function stopAutoSlide() {
        cancelAnimationFrame(progressAnimationFrame);
        clearTimeout(slideTimer);
    }

    function goToSlide(targetIndex) {
        if (targetIndex === currentIndex && videos[currentIndex].classList.contains('active')) return;

        const prevIndex = currentIndex;
        currentIndex = targetIndex;

        // Transition videos
        const prevVideo = videos[prevIndex];
        const nextVideo = videos[currentIndex];

        if (prevVideo) {
            prevVideo.classList.remove('active');
            setTimeout(() => {
                if (currentIndex !== prevIndex) {
                    prevVideo.pause();
                    prevVideo.currentTime = 0;
                }
            }, 600);
        }

        if (nextVideo) {
            nextVideo.classList.add('active');
            nextVideo.currentTime = 0;
            if (isPlaying) {
                nextVideo.play().catch(() => {});
            }
        }

        updateIndicators(currentIndex);

        if (isPlaying) {
            startAutoSlide();
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
            if (playPauseBtn) playPauseBtn.setAttribute('title', 'Pausar vídeo');
            startAutoSlide();
        } else {
            if (currentVideo) currentVideo.pause();
            if (pauseIcon) pauseIcon.style.display = 'none';
            if (playIcon) playIcon.style.display = 'block';
            if (playPauseBtn) playPauseBtn.setAttribute('title', 'Reproduzir vídeo');
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

/* ── 2. Sticky Hero Search Bar (Docks under Header on Scroll) ───────────── */
function initStickySearchBar() {
    const searchWrapper = document.getElementById('heroSearchWrapper');
    const searchBar = document.getElementById('heroSearchBar');
    const header = document.querySelector('.site-header');
    if (!searchWrapper || !searchBar) return;

    let isDocked = false;

    function handleScroll() {
        const headerBottom = header ? header.getBoundingClientRect().bottom : 58;
        const wrapperRect = searchWrapper.getBoundingClientRect();

        // Check if search wrapper reached the header bottom
        if (wrapperRect.top <= headerBottom) {
            if (!isDocked) {
                isDocked = true;
                searchWrapper.style.minHeight = `${searchBar.offsetHeight}px`;
                searchBar.classList.add('is-docked');
            }
            searchBar.style.top = `${Math.max(headerBottom, 0)}px`;
        } else {
            if (isDocked) {
                isDocked = false;
                searchBar.classList.remove('is-docked');
                searchBar.style.top = '';
                searchWrapper.style.minHeight = '';
            }
        }
    }

    window.addEventListener('scroll', handleScroll, { passive: true });
    window.addEventListener('resize', handleScroll, { passive: true });
    handleScroll();
}
