import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '7x-imoveis-secret-key-2026-super-secure'
    
    # Database — Supabase/PostgreSQL ou SQLite local como fallback
    basedir = os.path.abspath(os.path.dirname(__file__))
    _db_url = os.environ.get('DATABASE_URL') or ''
    # Supabase entrega 'postgres://' mas SQLAlchemy exige 'postgresql://'
    if _db_url.startswith('postgres://'):
        _db_url = _db_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = _db_url or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SITE_NAME = os.environ.get('SITE_NAME') or '7X Imóveis'
    SITE_SLOGAN = os.environ.get('SITE_SLOGAN') or 'Seu imóvel ideal com inteligência e exclusividade'
    CONTACT_PHONE = os.environ.get('CONTACT_PHONE') or '(11) 99999-7777'
    CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL') or 'contato@7ximoveis.com.br'
    CONTACT_ADDRESS = os.environ.get('CONTACT_ADDRESS') or 'Av. Paulista, 1000 - Bela Vista, São Paulo - SP'

    # Social & Direct Links (/links route) - Configurados via .env
    LINK_SITE_URL = os.environ.get('LINK_SITE_URL') or '/'
    LINK_INSTAGRAM_URL = os.environ.get('LINK_INSTAGRAM_URL') or 'https://instagram.com/7xpatrimonial'
    LINK_TIKTOK_URL = os.environ.get('LINK_TIKTOK_URL') or 'https://tiktok.com/@7xpatrimonial'
    LINK_WHATSAPP_URL = os.environ.get('LINK_WHATSAPP_URL') or 'https://wa.me/5511999997777'

    # Tecimob API Integration (https://swagger.tecimob.com.br)
    TECIMOB_API_TOKEN = os.environ.get('TECIMOB_API_TOKEN') or ''
    USE_TECIMOB_API = os.environ.get('USE_TECIMOB_API', 'false').lower() in ('true', '1', 't')

    # Admin Panel credentials (set in .env)
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or 'admin'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'changeme'

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'

class TestingConfig(Config):
    TESTING = True
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'

config_by_name = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'prod': ProductionConfig,
    'default': DevelopmentConfig
}

