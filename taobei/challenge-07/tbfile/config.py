import os


class BaseConfig(object):
    LISTENER = (os.getenv('APP_LISTEN_HOST', '0.0.0.0'),
                int(os.getenv('APP_LISTEN_PORT', '5040')))

    MONGO_URI = 'mongodb://localhost:27017/tbfile'

    ETCD_ADDR = 'localhost:2379'


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
