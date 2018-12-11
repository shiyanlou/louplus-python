class BaseConfig(object):
    LISTENER = ('0.0.0.0', 5040)

    MONGO_URI = 'mongodb://localhost:27017/tbfile'


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
