class BaseConfig(object):
    SECRET_KEY = '4bOoOz6GFmF5vVEPd0SvyOOt7m2b16l6'

    LISTENER = ('0.0.0.0', 5050)

    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@localhost:3306/tbweb?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FLASK_SQLALCHEMY_PER_PAGE = 20

    SERVICE_TBBUY = {
        'addresses': ['http://localhost:5030'],
    }
    SERVICE_TBFILE = {
        'addresses': ['http://localhost:5040'],
    }
    SERVICE_TBMALL = {
        'addresses': ['http://localhost:5020'],
    }
    SERVICE_TBUSER = {
        'addresses': ['http://localhost:5010'],
    }


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
