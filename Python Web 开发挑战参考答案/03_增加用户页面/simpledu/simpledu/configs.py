class BaseConfig:
    """配置类基类"""

    SECRET_KEY = 'makesure to set a very secret key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """开发环境配置类"""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost:3306/simpledu?charset=utf8'


class ProductionConfig(BaseConfig):
    """生产环境配置类"""

    pass


class TestingConfig(BaseConfig):
    """测试环境配置类"""

    pass


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
