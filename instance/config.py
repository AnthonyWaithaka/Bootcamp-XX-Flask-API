# /instance/config.py
"""Configuration options -
development
testing
staging
production
"""

import os

class Config(object):
    """Default configurations
    """
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET', "s1d24i67j8J12*#NCd8q32i@&*@&HID*WJD")
    POSTGRES = {
        'user': 'postgres',
        'pw': None,
        'db': 'flask_api',
        'host': 'localhost',
        'port': '5432',
    }
    SQLALCHEMY_DATABASE_URI = 'postgres://sicxvryjypbwar:e9cbb7b9a96329c2d040e30d5c37041c6f7cba6b84473bc4dee2a350c9420308@ec2-54-163-227-202.compute-1.amazonaws.com:5432/dd1vgtpq2iu0q9'
    #'postgresql://%(user)s:\
    #%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

class DevelopmentConfig(Config):
    """Development configurations
    """
    DEBUG = True

class TestingConfig(Config):
    """Testing configurations
    With separate database
    """
    TESTING = True
    POSTGRES = {
        'user': 'postgres',
        'pw': None,
        'db': 'test_db',
        'host': 'localhost',
        'port': '5432',
    }
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:\
    %(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    DEBUG = True

class StagingConfig(Config):
    """Staging configurations
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class ProductionConfig(Config):
    """Production Configurations
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}
