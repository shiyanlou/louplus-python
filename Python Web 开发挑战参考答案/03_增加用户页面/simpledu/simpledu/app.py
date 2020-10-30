from flask import Flask, render_template
from simpledu.configs import configs
from simpledu.models import db, Course
from simpledu.handlers import front, course, admin, user


def register_blueprints(app):
    """注册蓝图的函数
    """

    for bp in (front, course, admin, user):
        app.register_blueprint(bp)


def create_app(config):
    """此函数为工厂函数，用于创建应用对象并返回
    """

    app = Flask(__name__)
    app.config.from_object(configs.get(config))

    db.init_app(app)
    register_blueprints(app)

    return app
