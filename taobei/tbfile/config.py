class BaseConfig(object):
    SECRET_KEY = '4bOoOz6GFmF5vVEPd0SvyOOt7m2b16l6'

    LISTENER = ('0.0.0.0', 5040)

    MONGO_URI = 'mongodb://localhost:27017/tbfile'

    FLASK_SQLALCHEMY_PER_PAGE = 20


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
