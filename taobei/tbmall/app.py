from flask import Flask

from . import config
from . import db


def init_handlers(app):
    from . import handlers

    if app.env == 'production':
        app.register_error_handler(Exception, handlers.handle_error)

    app.register_blueprint(handlers.shop)
    app.register_blueprint(handlers.product)
    app.register_blueprint(handlers.favorite_product)


app = Flask(__name__)
app.config.from_object(config.configs.get(app.env))


db.init(app)

init_handlers(app)


if __name__ == '__main__':
    from gevent import pywsgi

    server = pywsgi.WSGIServer(app.config['LISTENER'], app)
    print('gevent WSGIServer listen on {} ...'.format(app.config['LISTENER']))
    server.serve_forever()
