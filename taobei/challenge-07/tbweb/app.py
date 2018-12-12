import threading

from flask import Flask

from tblib.etcd import init_etcd_client

from . import config


def init_handler(app):
    from .handlers import init

    init(app)


app = Flask(__name__)
app.config.from_object(config.configs.get(app.env))

threading.Thread(target=init_etcd_client, args=(app, )).start()

init_handler(app)


if __name__ == '__main__':
    from gevent import pywsgi

    server = pywsgi.WSGIServer(app.config['LISTENER'], app)
    print('gevent WSGIServer listen on {} ...'.format(app.config['LISTENER']))
    server.serve_forever()
