from flask import current_app
from flask_login import LoginManager

from tblib.handler import handle_error

from .common import common
from .product import product
from .shop import shop
from .user import user
from ..models import User
from ..services import TbUser


def init(app):
    app.register_blueprint(common)
    app.register_blueprint(product)
    app.register_blueprint(shop)
    app.register_blueprint(user)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(id):
        resp = TbUser(current_app).get_json(
            '/users/{}'.format(id), check_code=False)
        user = resp['data'].get('user')
        if user is None:
            return None
        else:
            return User(user)

    login_manager.login_view = 'user.login'

    login_manager.login_message = "请先登录"
