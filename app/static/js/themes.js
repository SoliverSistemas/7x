/* ==========================================================================
   7X Imoveis - Dark / Light Theme Toggle
   Arquivo independente, carregado antes dos outros scripts
   ========================================================================== */

(function () {
    var STORAGE_KEY = '7x_theme';
    var html = document.documentElement;

    // Aplica o tema apenas via atributo — nunca sobrescreve o SVG do botão
    function applyTheme(theme) {
        html.setAttribute('data-theme', theme);
        localStorage.setItem(STORAGE_KEY, theme);

        var btn = document.getElementById('theme-toggle-btn');
        if (!btn) return;
        btn.title = theme === 'dark' ? 'Mudar para tema claro' : 'Mudar para tema escuro';
        btn.setAttribute('aria-label', btn.title);
    }

    // Aplica imediatamente (sem esperar DOMContentLoaded) para evitar flash
    var saved = localStorage.getItem(STORAGE_KEY) || 'dark';
    html.setAttribute('data-theme', saved);

    // Conecta o evento de clique após o DOM estar pronto
    document.addEventListener('DOMContentLoaded', function () {
        applyTheme(saved);

        var btn = document.getElementById('theme-toggle-btn');
        if (!btn) return;

        btn.addEventListener('click', function () {
            var current = html.getAttribute('data-theme') || 'dark';
            applyTheme(current === 'dark' ? 'light' : 'dark');

            // Micro-animação de rotação ao clicar
            btn.classList.add('spinning');
            setTimeout(function () { btn.classList.remove('spinning'); }, 500);
        });
    });
})();

