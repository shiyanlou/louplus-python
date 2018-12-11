from tblib.handler import handle_error_json

from .cart_product import cart_product
from .order import order


def init(app):
    app.register_error_handler(Exception, handle_error_json)

    app.register_blueprint(cart_product)
    app.register_blueprint(order)
