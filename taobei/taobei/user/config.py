class BaseConfig(object):
    SECRET_KEY = '4bOoOz6GFmF5vVEPd0SvyOOt7m2b16l6'

    LISTENER = ('0.0.0.0', 5010)

    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@localhost:3306/taobei?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
