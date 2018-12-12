from tblib.handler import handle_error_json

from .shop import shop
from .product import product
from .favorite_product import favorite_product


def init(app):
    app.register_error_handler(Exception, handle_error_json)

    app.register_blueprint(shop)
    app.register_blueprint(product)
    app.register_blueprint(favorite_product)
