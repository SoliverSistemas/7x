from flask import Flask, render_template
from config import config_by_name

def create_app(config_name='dev'):
    """
    Application Factory Pattern for 7X Imóveis Flask App.
    """
    app = Flask(__name__, instance_relative_config=True)
    
    # Load Configuration
    if isinstance(config_name, str):
        app.config.from_object(config_by_name.get(config_name, config_by_name['default']))
    else:
        app.config.from_object(config_name)
    
    # Register Custom Template Filters
    @app.template_filter('currency')
    def currency_format(value):
        try:
            val = float(value)
            return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except (ValueError, TypeError):
            return "R$ 0,00"

    @app.template_filter('area_format')
    def area_format(value):
        try:
            return f"{int(value)} m²"
        except (ValueError, TypeError):
            return "0 m²"

    # Register Context Processors (global variables for templates)
    @app.context_processor
    def inject_global_vars():
        return {
            'site_name': app.config.get('SITE_NAME', '7X Imóveis'),
            'site_slogan': app.config.get('SITE_SLOGAN', ''),
            'contact_phone': app.config.get('CONTACT_PHONE', ''),
            'contact_email': app.config.get('CONTACT_EMAIL', ''),
            'contact_address': app.config.get('CONTACT_ADDRESS', '')
        }

    # Register Blueprints
    from app.routes.main import main_bp
    from app.routes.properties import properties_bp
    from app.routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(properties_bp, url_prefix='/imoveis')
    app.register_blueprint(api_bp, url_prefix='/api')

    # Register Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    return app
