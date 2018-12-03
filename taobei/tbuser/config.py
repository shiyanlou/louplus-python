class BaseConfig(object):
    LISTENER = ('0.0.0.0', 5010)

    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@localhost:3306/tbuser?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PAGINATION_PER_PAGE = 20


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
