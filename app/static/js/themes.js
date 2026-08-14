/* ==========================================================================
   7X Imoveis - Dark / Light Theme Toggle
   Arquivo independente, carregado antes dos outros scripts
   ========================================================================== */

(function () {
    var STORAGE_KEY = '7x_theme';
    var html = document.documentElement;

    // Aplica o tema e atualiza o icone do botao
    function applyTheme(theme) {
        html.setAttribute('data-theme', theme);
        localStorage.setItem(STORAGE_KEY, theme);

        var btn = document.getElementById('theme-toggle-btn');
        if (!btn) return;

        if (theme === 'dark') {
            btn.textContent = '\u2600\uFE0F';  // sol = clique para ir ao claro
            btn.title = 'Mudar para tema claro';
        } else {
            btn.textContent = '\uD83C\uDF19';  // lua = clique para ir ao escuro
            btn.title = 'Mudar para tema escuro';
        }
    }

    // Aplica imediatamente (sem esperar DOMContentLoaded) para evitar flash
    var saved = localStorage.getItem(STORAGE_KEY) || 'dark';
    html.setAttribute('data-theme', saved);

    // Quando o DOM estiver pronto, conecta o evento e atualiza o icone
    document.addEventListener('DOMContentLoaded', function () {
        applyTheme(saved);

        var btn = document.getElementById('theme-toggle-btn');
        if (!btn) return;

        btn.addEventListener('click', function () {
            var current = html.getAttribute('data-theme') || 'dark';
            applyTheme(current === 'dark' ? 'light' : 'dark');
        });
    });
})();
