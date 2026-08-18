/* ============================================================
   7X Chatbot — chatbot.js
   Motor de conversação rule-based (árvore de decisão)
   ============================================================ */

(function () {
    'use strict';

    /* ── Configuração ──────────────────────────────────────── */
    const CFG = {
        botName:    'Ana · 7X',
        typing:     700,        // ms de delay "digitando..."
        leadUrl:    '/chatbot/lead',
        waNumber:   document.documentElement.dataset.whatsapp || '5521990570909',
    };

    /* ── Estado interno ─────────────────────────────────────── */
    const state = {
        step:    'start',
        data:    {},           // acumula dados do lead
        history: [],           // log textual para salvar como "message"
    };

    /* ── Árvore de decisão ──────────────────────────────────── */
    const FLOW = {

        start: {
            bot: 'Olá! 👋 Eu sou a <strong>Ana</strong>, assistente virtual da <strong>7X Imóveis</strong>.<br>Como posso te ajudar hoje?',
            replies: [
                { label: '🔍 Buscar Imóvel',      next: 'search_purpose' },
                { label: '📅 Agendar Visita',      next: 'schedule_start' },
                { label: '💬 Falar com Corretor',  next: 'contact'        },
                { label: 'ℹ️ Sobre a 7X',           next: 'about'          },
            ],
        },

        /* ── Busca ── */
        search_purpose: {
            bot: 'Ótimo! Você busca um imóvel para:',
            replies: [
                { label: '🏷️ Comprar', next: 'search_type', data: { purpose: 'Venda'    } },
                { label: '🔑 Alugar',  next: 'search_type', data: { purpose: 'Aluguel'  } },
                { label: '⬅️ Voltar',  next: 'start' },
            ],
        },

        search_type: {
            bot: 'Que tipo de imóvel você procura?',
            replies: [
                { label: '🏠 Casa',        next: 'search_go', data: { type: 'Casa'        } },
                { label: '🏢 Apartamento', next: 'search_go', data: { type: 'Apartamento' } },
                { label: '🌳 Terreno',     next: 'search_go', data: { type: 'Terreno'     } },
                { label: '🏪 Comercial',   next: 'search_go', data: { type: 'Comercial'   } },
                { label: '⬅️ Voltar',      next: 'search_purpose' },
            ],
        },

        search_go: {
            bot: (s) => {
                const url = buildSearchUrl(s.data);
                return `Encontrei imóveis para você! 🎉<br>
                        <a href="${url}" style="color:#c9ac77;font-weight:700;text-decoration:underline;">
                        Ver ${s.data.type || 'imóveis'} para ${s.data.purpose || 'comprar/alugar'} →</a>`;
            },
            replies: [
                { label: '🔄 Nova Busca', next: 'search_purpose' },
                { label: '📅 Agendar Visita', next: 'schedule_start' },
                { label: '🏠 Menu Principal', next: 'start' },
            ],
        },

        /* ── Agendamento ── */
        schedule_start: {
            bot: 'Adorei! Para agendar sua visita, preciso de algumas informações.<br>Qual é o <strong>seu nome</strong>?',
            input: true,
            inputPlaceholder: 'Digite seu nome…',
            onInput: (val, s) => {
                s.data.name = val;
                s.history.push(`Nome: ${val}`);
                return 'schedule_phone';
            },
        },

        schedule_phone: {
            bot: (s) => `Prazer, <strong>${s.data.name}</strong>! 😊<br>Agora me diga seu <strong>WhatsApp ou telefone</strong>:`,
            input: true,
            inputPlaceholder: 'Ex: (21) 99999-9999',
            onInput: (val, s) => {
                s.data.phone = val;
                s.history.push(`Telefone: ${val}`);
                return 'schedule_property';
            },
        },

        schedule_property: {
            bot: 'Que imóvel te interessa? Pode ser o endereço, referência ou código:',
            input: true,
            inputPlaceholder: 'Ex: Ref. 1234, Rua das Flores…',
            onInput: (val, s) => {
                s.data.property = val;
                s.history.push(`Imóvel: ${val}`);
                return 'schedule_confirm';
            },
        },

        schedule_confirm: {
            bot: async (s) => {
                s.history.push(`Página: ${window.location.href}`);
                await saveLead(s);
                return `✅ <strong>Perfeito!</strong> Recebemos sua solicitação.<br>
                        Em breve um de nossos corretores entrará em contato com você no número <strong>${s.data.phone}</strong>.<br><br>
                        Enquanto isso, pode visitar nosso catálogo completo!`;
            },
            replies: [
                { label: '📂 Ver Catálogo', next: '__link', href: '/imoveis' },
                { label: '💬 Falar agora pelo WhatsApp', next: '__wa' },
                { label: '🏠 Menu Principal', next: 'start' },
            ],
        },

        /* ── Contato ── */
        contact: {
            bot: (s) => `Nossos corretores estão prontos para te atender! 😊<br><br>
                         📞 <a href="tel:${CFG.waNumber}" style="color:#c9ac77;font-weight:700;">${formatPhone(CFG.waNumber)}</a><br>
                         💬 <a href="https://wa.me/${CFG.waNumber}" target="_blank" style="color:#c9ac77;font-weight:700;">WhatsApp → Clique aqui</a>`,
            replies: [
                { label: '🏠 Menu Principal', next: 'start' },
            ],
        },

        /* ── Sobre ── */
        about: {
            bot: `A <strong>7X Imóveis</strong> é especializada em imóveis de alto padrão.<br>
                  Oferecemos uma seleção curada de propriedades exclusivas com atendimento personalizado e total transparência.<br><br>
                  Nosso time de especialistas está pronto para encontrar o imóvel ideal para você. 🏡`,
            replies: [
                { label: '🔍 Buscar Imóvel',    next: 'search_purpose' },
                { label: '💬 Falar com Corretor', next: 'contact' },
                { label: '🏠 Menu Principal',    next: 'start' },
            ],
        },
    };

    /* ── Utilitários ─────────────────────────────────────────── */
    function buildSearchUrl(data) {
        const params = new URLSearchParams();
        if (data.purpose) params.set('purpose', data.purpose);
        if (data.type)    params.set('type', data.type);
        return '/imoveis?' + params.toString();
    }

    function formatPhone(num) {
        // Formata 5521990570909 → +55 (21) 99057-0909
        const d = num.replace(/\D/g, '');
        if (d.length === 13) {
            return `+${d.slice(0,2)} (${d.slice(2,4)}) ${d.slice(4,9)}-${d.slice(9)}`;
        }
        return num;
    }

    async function saveLead(s) {
        try {
            await fetch(CFG.leadUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name:    s.data.name    || '',
                    phone:   s.data.phone   || '',
                    message: s.history.join(' | '),
                    page:    window.location.href,
                }),
            });
        } catch (_) { /* silencioso */ }
    }

    /* ── DOM ─────────────────────────────────────────────────── */
    const $toggle  = document.getElementById('chatbotToggle');
    const $window  = document.getElementById('chatbotWindow');
    const $msgs    = document.getElementById('chatMessages');
    const $input   = document.getElementById('chatInput');
    const $send    = document.getElementById('chatSendBtn');
    const $badge   = document.getElementById('chatNotifBadge');
    const $close   = document.getElementById('chatClose');

    if (!$toggle || !$window) return; // chatbot não presente na página

    let isOpen = false;
    let inputMode = false;   // true = aguardando texto do usuário
    let inputCallback = null;

    /* ── Toggle abrir/fechar ──────────────────────────────────── */
    function open() {
        isOpen = true;
        $window.classList.add('is-open');
        $toggle.classList.add('is-open');
        $badge.classList.add('hidden');
        if ($msgs.children.length === 0) goTo('start');
    }

    function close() {
        isOpen = false;
        $window.classList.remove('is-open');
        $toggle.classList.remove('is-open');
    }

    $toggle.addEventListener('click', () => isOpen ? close() : open());
    $close.addEventListener('click', close);

    /* Fechar ao clicar fora */
    document.addEventListener('click', (e) => {
        if (isOpen && !$window.contains(e.target) && !$toggle.contains(e.target)) {
            close();
        }
    });

    /* ── Renderização ────────────────────────────────────────── */
    function addBubble(html, type = 'bot') {
        const el = document.createElement('div');
        el.className = `chat-bubble chat-bubble--${type}`;
        el.innerHTML = html;
        $msgs.appendChild(el);
        scrollBottom();
        return el;
    }

    function addQuickReplies(replies) {
        const wrap = document.createElement('div');
        wrap.className = 'chat-quick-replies';
        replies.forEach(r => {
            const btn = document.createElement('button');
            btn.className = 'chat-qr-btn';
            btn.textContent = r.label;
            btn.addEventListener('click', (e) => {
                e.stopPropagation(); // evita que o clique feche o chat
                handleReply(r);
            });
            wrap.appendChild(btn);
        });
        $msgs.appendChild(wrap);
        scrollBottom();
    }

    function showTyping() {
        const el = document.createElement('div');
        el.className = 'chat-typing';
        el.innerHTML = '<span></span><span></span><span></span>';
        el.id = 'chatTyping';
        $msgs.appendChild(el);
        scrollBottom();
        return el;
    }

    function removeTyping() {
        const el = document.getElementById('chatTyping');
        if (el) el.remove();
    }

    function scrollBottom() {
        $msgs.scrollTop = $msgs.scrollHeight;
    }

    function setInputMode(active, placeholder = 'Digite sua resposta…') {
        inputMode = active;
        $input.disabled = !active;
        $input.placeholder = active ? placeholder : 'Selecione uma opção acima…';
        $send.disabled = !active;
        if (active) setTimeout(() => $input.focus(), 100);
    }

    /* ── Navegar para um step ────────────────────────────────── */
    async function goTo(stepId) {
        const step = FLOW[stepId];
        if (!step) return;
        state.step = stepId;

        setInputMode(false);
        const typing = showTyping();
        await delay(CFG.typing);
        removeTyping();

        /* Mensagem do bot (pode ser função async) */
        let msg = typeof step.bot === 'function'
            ? await step.bot(state)
            : step.bot;

        if (typeof msg !== 'string') msg = '…';
        addBubble(msg, 'bot');

        /* Respostas rápidas ou input */
        if (step.input) {
            setInputMode(true, step.inputPlaceholder);
            inputCallback = step.onInput;
        } else if (step.replies && step.replies.length) {
            addQuickReplies(step.replies);
            setInputMode(false);
        }
    }

    /* ── Lidar com reply clicado ─────────────────────────────── */
    function handleReply(reply) {
        /* Remove todos os botões de resposta rápida */
        $msgs.querySelectorAll('.chat-quick-replies').forEach(el => el.remove());

        /* Adiciona balão do usuário */
        addBubble(reply.label, 'user');
        state.history.push(reply.label);

        /* Mescla dados extras do reply */
        if (reply.data) Object.assign(state.data, reply.data);

        /* Links especiais */
        if (reply.next === '__link' && reply.href) {
            window.location.href = reply.href;
            return;
        }
        if (reply.next === '__wa') {
            window.open(`https://wa.me/${CFG.waNumber}`, '_blank');
            return;
        }

        goTo(reply.next);
    }

    /* ── Envio de texto livre ────────────────────────────────── */
    function handleSend() {
        if (!inputMode || !inputCallback) return;
        const val = $input.value.trim();
        if (!val) return;

        $msgs.querySelectorAll('.chat-quick-replies').forEach(el => el.remove());
        addBubble(val, 'user');
        $input.value = '';
        setInputMode(false);

        const nextStep = inputCallback(val, state);
        inputCallback = null;

        if (nextStep instanceof Promise) {
            nextStep.then(step => step && goTo(step));
        } else if (nextStep) {
            goTo(nextStep);
        }
    }

    $send.addEventListener('click', handleSend);
    $input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(); }
    });

    /* ── Helpers ─────────────────────────────────────────────── */
    function delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /* ── Auto-abrir após delay (primeira visita) ─────────────── */
    const chatSeen = sessionStorage.getItem('7x_chat_seen');
    if (!chatSeen) {
        setTimeout(() => {
            $badge.classList.remove('hidden');
            $badge.textContent = '1';
        }, 5000);
        sessionStorage.setItem('7x_chat_seen', '1');
    }

})();
