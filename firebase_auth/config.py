import os

class Config:
    SECRET_KEY = os.environ.get("SECEET_KEY") or 'my_secret_key'

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    WEB_API_KEY = os.environ.get('WEB_API_KEY')
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    WTF_CSRF_ENABLED = True

class TestingConfig(Config):
    TESTING = True
    WEB_API_KEY = os.environ.get('WEB_API_KEY')
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    WTF_CSRF_ENABLED = False