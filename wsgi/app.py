from wsgiref.simple_server import make_server


def index():
    return b'index page', '200 OK', [('Content-Type', 'text/html')]

def api():
    return b'{"name": "Aiden", "email": "luojin@simplecloud.cn"}', '201 Created', [('Content-Type', 'application/json')]

def not_found():
    return b'404 page', '404 NOT FOUND', [('Content-Type', 'text/plain')]


URL_PATTERNS= (
    ('/', index),
    ('api', api),
    ('course', not_found)
)


class Flask:

    def route(self, path):
        path = path.split('/')[1]
        for url, controller in URL_PATTERNS:
            if path in url:
                return controller

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO','/')
        controller = self.route(path)
        if controller :
            body, status, headers = controller()
            start_response(status, headers)
            return [body]
        else:
            start_response('404 NOT FOUND',[('Content-type', 'text/plain')])
            return [b'Page dose not exists!']


if __name__ == '__main__':
    app = Flask()
    httpd = make_server('', 8091, app)
    print('Serving on port 8091...')
    httpd.serve_forever()
