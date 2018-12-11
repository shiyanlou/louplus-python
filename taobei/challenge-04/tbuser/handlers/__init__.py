from tblib.handler import handle_error_json

from .user import user
from .address import address
from .wallet_transaction import wallet_transaction


def init(app):
    app.register_error_handler(Exception, handle_error_json)

    app.register_blueprint(user)
    app.register_blueprint(address)
    app.register_blueprint(wallet_transaction)
