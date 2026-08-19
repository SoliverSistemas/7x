from flask import Flask, render_template
from config import config_by_name
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

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
        
    # Initialize Database
    db.init_app(app)
    migrate.init_app(app, db)
    
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
        import re
        wa_url = app.config.get('LINK_WHATSAPP_URL', 'https://wa.me/5521990570909')
        # Extrai só os dígitos do número do WhatsApp (ex: 5521990570909)
        wa_number_match = re.search(r'wa\.me/(\d+)', wa_url)
        wa_number = wa_number_match.group(1) if wa_number_match else '5521990570909'
        return {
            'site_name': app.config.get('SITE_NAME', '7X Imóveis'),
            'site_slogan': app.config.get('SITE_SLOGAN', ''),
            'contact_phone': app.config.get('CONTACT_PHONE', ''),
            'contact_phone_2': app.config.get('CONTACT_PHONE_2', ''),
            'contact_email': app.config.get('CONTACT_EMAIL', ''),
            'contact_address': app.config.get('CONTACT_ADDRESS', ''),
            'whatsapp_url': wa_url,
            'whatsapp_url_2': app.config.get('LINK_WHATSAPP_URL_2', ''),
            'whatsapp_number': wa_number,
        }

    # Register Blueprints
    from app.routes.main import main_bp
    from app.routes.properties import properties_bp
    from app.routes.api import api_bp
    from app.routes.admin import admin_bp
    from app.routes.agents import agents_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(properties_bp, url_prefix='/imoveis')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(agents_bp)

    # Register Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    # Import models so Flask-Migrate can detect them
    with app.app_context():
        from app.models.db_models import Property, ExclusiveCollection, Lancamento, AgentProfile  # noqa: F401

    return app
