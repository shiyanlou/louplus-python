from tblib.handler import handle_error

from .cart_product import cart_product
from .order import order


def init(app):
    app.register_error_handler(Exception, handle_error)

    app.register_blueprint(cart_product)
    app.register_blueprint(order)
