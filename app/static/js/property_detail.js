/* ==========================================================================
   7X Patrimonial - Property Detail Page Interactive Scripts
   - Fullscreen Photo Lightbox with Thumbnails & Keyboard navigation
   - Reference Code One-Click Copy
   - Social & WhatsApp Share
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    initPropertyLightbox();
    initCopyReference();
    initShareButtons();
});

/* ── 1. Fullscreen Lightbox Gallery ──────────────────────────────────────── */
function initPropertyLightbox() {
    const lightboxModal = document.getElementById('propertyLightboxModal');
    if (!lightboxModal) return;

    const lightboxImg = document.getElementById('lightboxActiveImage');
    const lightboxCounter = document.getElementById('lightboxCounter');
    const thumbContainer = document.getElementById('lightboxThumbs');
    const prevBtn = document.getElementById('lightboxPrevBtn');
    const nextBtn = document.getElementById('lightboxNextBtn');
    const closeBtn = document.getElementById('lightboxCloseBtn');

    // Collect all gallery image sources
    const galleryItems = Array.from(document.querySelectorAll('[data-lightbox-src]'));
    if (galleryItems.length === 0) return;

    const images = galleryItems.map(el => el.getAttribute('data-lightbox-src'));
    let activeIndex = 0;

    // Populate thumbnails
    if (thumbContainer) {
        thumbContainer.innerHTML = '';
        images.forEach((src, idx) => {
            const thumb = document.createElement('button');
            thumb.className = `lightbox-thumb-btn ${idx === 0 ? 'active' : ''}`;
            thumb.setAttribute('aria-label', `Foto ${idx + 1}`);
            thumb.innerHTML = `<img src="${src}" alt="Miniatura ${idx + 1}" loading="lazy">`;
            thumb.addEventListener('click', () => showImage(idx));
            thumbContainer.appendChild(thumb);
        });
    }

    function showImage(index) {
        if (index < 0) index = images.length - 1;
        if (index >= images.length) index = 0;
        activeIndex = index;

        if (lightboxImg) {
            lightboxImg.style.opacity = '0';
            lightboxImg.src = images[activeIndex];
            lightboxImg.onload = () => {
                lightboxImg.style.opacity = '1';
            };
        }

        if (lightboxCounter) {
            lightboxCounter.textContent = `${activeIndex + 1} / ${images.length}`;
        }

        // Update thumbnails active state
        if (thumbContainer) {
            const thumbs = thumbContainer.querySelectorAll('.lightbox-thumb-btn');
            thumbs.forEach((t, i) => {
                t.classList.toggle('active', i === activeIndex);
                if (i === activeIndex) {
                    t.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
                }
            });
        }
    }

    function openLightbox(index = 0) {
        lightboxModal.classList.add('active');
        document.body.style.overflow = 'hidden';
        showImage(index);
    }

    function closeLightbox() {
        lightboxModal.classList.remove('active');
        document.body.style.overflow = '';
    }

    // Trigger buttons
    galleryItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const idx = parseInt(item.getAttribute('data-lightbox-index') || '0', 10);
            openLightbox(idx);
        });
    });

    const openGalleryTrigger = document.getElementById('openFullGalleryBtn');
    if (openGalleryTrigger) {
        openGalleryTrigger.addEventListener('click', (e) => {
            e.preventDefault();
            openLightbox(0);
        });
    }

    if (closeBtn) closeBtn.addEventListener('click', closeLightbox);
    if (prevBtn) prevBtn.addEventListener('click', () => showImage(activeIndex - 1));
    if (nextBtn) nextBtn.addEventListener('click', () => showImage(activeIndex + 1));

    // Close on overlay click
    lightboxModal.addEventListener('click', (e) => {
        if (e.target === lightboxModal || e.target.classList.contains('lightbox-backdrop')) {
            closeLightbox();
        }
    });

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (!lightboxModal.classList.contains('active')) return;
        if (e.key === 'Escape') closeLightbox();
        if (e.key === 'ArrowLeft') showImage(activeIndex - 1);
        if (e.key === 'ArrowRight') showImage(activeIndex + 1);
    });
}

/* ── 2. Reference Code One-Click Copy ────────────────────────────────────── */
function initCopyReference() {
    const copyBtns = document.querySelectorAll('.copy-reference-btn');
    copyBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const refCode = btn.getAttribute('data-ref') || btn.innerText.trim();
            if (!refCode) return;

            navigator.clipboard.writeText(refCode).then(() => {
                const originalHtml = btn.innerHTML;
                btn.innerHTML = `<span style="color: var(--primary);">✓ Copiado!</span>`;
                setTimeout(() => {
                    btn.innerHTML = originalHtml;
                }, 2000);
            }).catch(() => {});
        });
    });
}

/* ── 3. Share Buttons ────────────────────────────────────────────────────── */
function initShareButtons() {
    const shareLinkBtn = document.getElementById('shareLinkBtn');
    if (shareLinkBtn) {
        shareLinkBtn.addEventListener('click', (e) => {
            e.preventDefault();
            if (navigator.share) {
                navigator.share({
                    title: document.title,
                    url: window.location.href
                }).catch(() => {});
            } else {
                navigator.clipboard.writeText(window.location.href).then(() => {
                    const originalText = shareLinkBtn.innerText;
                    shareLinkBtn.innerText = 'Link Copiado!';
                    setTimeout(() => { shareLinkBtn.innerText = originalText; }, 2000);
                });
            }
        });
    }
}
