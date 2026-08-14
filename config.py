import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '7x-imoveis-secret-key-2026-super-secure'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SITE_NAME = '7X Imóveis'
    SITE_SLOGAN = 'Seu imóvel ideal com inteligência e exclusividade'
    CONTACT_PHONE = '(11) 99999-7777'
    CONTACT_EMAIL = 'contato@7ximoveis.com.br'
    CONTACT_ADDRESS = 'Av. Paulista, 1000 - Bela Vista, São Paulo - SP'

    # Tecimob API Integration (https://swagger.tecimob.com.br)
    TECIMOB_API_TOKEN = os.environ.get('TECIMOB_API_TOKEN') or ''
    USE_TECIMOB_API = os.environ.get('USE_TECIMOB_API', 'false').lower() in ('true', '1', 't')

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

