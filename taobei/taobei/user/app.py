from flask import Flask

from . import config
from . import db
from . import handlers

app = Flask(__name__)

app.config.from_object(config.configs.get(app.env))

db.init(app)

app.register_blueprint(handlers.user)

if __name__ == '__main__':
    from gevent import pywsgi

    server = pywsgi.WSGIServer(app.config['LISTENER'], app)
    print('gevent WSGIServer listen on {} ...'.format(app.config['LISTENER']))
    server.serve_forever()
