import os


class BaseConfig(object):
    LISTENER = (os.getenv('APP_LISTEN_HOST', '0.0.0.0'),
                int(os.getenv('APP_LISTEN_PORT', '5010')))

    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@localhost:3306/tbuser?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ETCD_ADDR = 'localhost:2379'

    PAGINATION_PER_PAGE = 20


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
