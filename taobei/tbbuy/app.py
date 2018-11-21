from importlib import import_module

from flask import Flask
from tblib import model

from . import config
from .handlers import init as init_handlers


app = Flask(__name__)
app.config.from_object(config.configs.get(app.env))


model.init(app)
import_module('.models', __package__)

init_handlers(app)


if __name__ == '__main__':
    from gevent import pywsgi

    server = pywsgi.WSGIServer(app.config['LISTENER'], app)
    print('gevent WSGIServer listen on {} ...'.format(app.config['LISTENER']))
    server.serve_forever()
