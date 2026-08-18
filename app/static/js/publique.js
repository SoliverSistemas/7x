/* ==========================================================================
   7X Imóveis - Publique seu Imóvel — JavaScript
   Monta a mensagem do formulário e abre o WhatsApp com o conteúdo.
   ========================================================================== */

(function () {
    'use strict';

    // ── Número de WhatsApp da imobiliária (mesmo do .env LINK_WHATSAPP_URL) ──
    const WA_NUMBER = '5521990570909';

    // ── Máscara de telefone (XX) XXXXX-XXXX ──────────────────────────────────
    const whatsappInput = document.getElementById('pub-whatsapp');
    if (whatsappInput) {
        whatsappInput.addEventListener('input', function () {
            let v = this.value.replace(/\D/g, '').substring(0, 11);
            if (v.length > 6) {
                v = `(${v.substring(0, 2)}) ${v.substring(2, 7)}-${v.substring(7)}`;
            } else if (v.length > 2) {
                v = `(${v.substring(0, 2)}) ${v.substring(2)}`;
            } else if (v.length > 0) {
                v = `(${v}`;
            }
            this.value = v;
        });
    }

    // ── Máscara de valor monetário ────────────────────────────────────────────
    const valorInput = document.getElementById('pub-valor');
    if (valorInput) {
        valorInput.addEventListener('input', function () {
            let raw = this.value.replace(/\D/g, '');
            if (!raw) { this.value = ''; return; }
            // Formata como R$ 1.234.567
            const n = parseInt(raw, 10);
            this.value = 'R$ ' + n.toLocaleString('pt-BR');
        });
    }

    // ── Highlight dos radio cards ao clicar ───────────────────────────────────
    document.querySelectorAll('.radio-card').forEach(function (card) {
        card.addEventListener('click', function () {
            document.querySelectorAll('.radio-card').forEach(c => c.classList.remove('checked'));
            this.classList.add('checked');
        });
    });

    // ── Validação de campo obrigatório ────────────────────────────────────────
    function validateField(id, errorId, msg) {
        const el = document.getElementById(id);
        const errEl = document.getElementById(errorId);
        if (!el || !errEl) return true;
        const val = el.value.trim();
        if (!val) {
            el.classList.add('is-invalid');
            errEl.textContent = msg;
            return false;
        }
        el.classList.remove('is-invalid');
        errEl.textContent = '';
        return true;
    }

    // ── Limpa erros ao digitar ────────────────────────────────────────────────
    ['pub-nome', 'pub-whatsapp', 'pub-tipo', 'pub-valor', 'pub-endereco'].forEach(function (id) {
        const el = document.getElementById(id);
        if (el) {
            el.addEventListener('input', function () {
                this.classList.remove('is-invalid');
                const errEl = document.getElementById('err-' + id.replace('pub-', ''));
                if (errEl) errEl.textContent = '';
            });
        }
    });

    // ── Função principal: monta mensagem e abre WhatsApp ─────────────────────
    function buildWhatsAppMessage(data) {
        const line = (label, val) => val ? `• *${label}:* ${val}\n` : '';

        let msg = '🏠 *SOLICITAÇÃO DE ANÚNCIO — 7X Patrimonial*\n';
        msg += '─────────────────────────────\n\n';

        msg += '👤 *DADOS DO PROPRIETÁRIO*\n';
        msg += line('Nome', data.nome);
        msg += line('WhatsApp', data.whatsapp);
        msg += line('E-mail', data.email);
        msg += '\n';

        msg += '🏷️ *TIPO DE NEGÓCIO*\n';
        msg += line('Finalidade', data.finalidade);
        msg += '\n';

        msg += '🏠 *INFORMAÇÕES DO IMÓVEL*\n';
        msg += line('Tipo', data.tipo);
        msg += line('Endereço / Localização', data.endereco);
        msg += line('Valor', data.valor);
        if (data.area)    msg += line('Área', data.area + ' m²');
        if (data.quartos) msg += line('Quartos', data.quartos);
        if (data.suites)  msg += line('Suítes', data.suites);
        if (data.vagas)   msg += line('Vagas de garagem', data.vagas);
        msg += '\n';

        if (data.diferenciais && data.diferenciais.length > 0) {
            msg += '✨ *DIFERENCIAIS*\n';
            msg += data.diferenciais.map(d => `  ✅ ${d}`).join('\n') + '\n\n';
        }

        if (data.descricao) {
            msg += '📝 *INFORMAÇÕES ADICIONAIS*\n';
            msg += data.descricao + '\n\n';
        }

        msg += '─────────────────────────────\n';
        msg += '_Mensagem enviada pelo site 7X Patrimonial_';

        return msg;
    }

    // ── Submit Handler ────────────────────────────────────────────────────────
    const form = document.getElementById('publique-imovel-form');
    if (!form) return;

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        // Validações
        const v1 = validateField('pub-nome',      'err-nome',      'Por favor, informe seu nome.');
        const v2 = validateField('pub-whatsapp',  'err-whatsapp',  'Por favor, informe seu WhatsApp.');
        const v3 = validateField('pub-tipo',      'err-tipo',      'Selecione o tipo de imóvel.');
        const v4 = validateField('pub-valor',     'err-valor',     'Informe o valor pretendido.');
        const v5 = validateField('pub-endereco',  'err-endereco',  'Informe o endereço ou bairro.');

        if (!v1 || !v2 || !v3 || !v4 || !v5) {
            // Scroll suave até o primeiro campo inválido
            const firstInvalid = form.querySelector('.is-invalid');
            if (firstInvalid) {
                firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                firstInvalid.focus();
            }
            return;
        }

        // Coleta diferenciais selecionados
        const diferenciais = Array.from(
            form.querySelectorAll('input[name="diferenciais"]:checked')
        ).map(cb => cb.value);

        // Coleta a finalidade selecionada
        const finalidadeEl = form.querySelector('input[name="finalidade"]:checked');

        // Monta objeto de dados
        const data = {
            nome:        document.getElementById('pub-nome').value.trim(),
            whatsapp:    document.getElementById('pub-whatsapp').value.trim(),
            email:       document.getElementById('pub-email').value.trim(),
            finalidade:  finalidadeEl ? finalidadeEl.value : 'Venda',
            tipo:        document.getElementById('pub-tipo').value,
            valor:       document.getElementById('pub-valor').value.trim(),
            endereco:    document.getElementById('pub-endereco').value.trim(),
            area:        document.getElementById('pub-area').value.trim(),
            quartos:     document.getElementById('pub-quartos').value,
            suites:      document.getElementById('pub-suites').value,
            vagas:       document.getElementById('pub-vagas').value,
            diferenciais: diferenciais,
            descricao:   document.getElementById('pub-descricao').value.trim(),
        };

        // Monta URL do WhatsApp
        const msg = buildWhatsAppMessage(data);
        const encoded = encodeURIComponent(msg);
        const waUrl = `https://wa.me/${WA_NUMBER}?text=${encoded}`;

        // Feedback visual no botão antes de abrir
        const btn = document.getElementById('btn-publique-submit');
        if (btn) {
            btn.textContent = '✅ Abrindo WhatsApp...';
            btn.disabled = true;
            btn.style.opacity = '0.85';
            setTimeout(function () {
                btn.disabled = false;
                btn.style.opacity = '';
                btn.innerHTML = `
                    <svg class="btn-wa-icon" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413Z"/>
                    </svg>
                    Enviar pelo WhatsApp
                    <svg class="btn-arrow-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                        <path d="M5 12h14M12 5l7 7-7 7"/>
                    </svg>`;
            }, 3000);
        }

        // Abre o WhatsApp em nova aba
        window.open(waUrl, '_blank', 'noopener,noreferrer');
    });

    // ── Estilo de invalid field via JS ────────────────────────────────────────
    const style = document.createElement('style');
    style.textContent = `
        .form-control.is-invalid,
        .form-select.is-invalid {
            border-color: #ef4444 !important;
            box-shadow: 0 0 0 3px rgba(239,68,68,0.15) !important;
        }
    `;
    document.head.appendChild(style);

})();
