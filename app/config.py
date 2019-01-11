import os


class Config(object):
    """
    Base config class.
    """
    DEBUG = False
    TESTING = False

    SECRET_KEY = 'fd8d782c2633851ce9be7329d3d6d126c1827450fdcc4eba5247e172f4d5f7f8ce1d0d353ed20890f19a7d6f28a46255'
    LOGFILE_PATH = os.environ.get('LOGFILE_PATH', 'log/app.log')


class LocalConfig(Config):
    """
    local config.
    """
    DEBUG = True


class DevelopmentConfig(Config):
    """
    dev environment config.
    """
    DEBUG = True


class TestingConfig(Config):
    """
    testing config.
    """
    TESTING = True


class ProductionConfig(Config):
    """
    production config.
    """
    pass
