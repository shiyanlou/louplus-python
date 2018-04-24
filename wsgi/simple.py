from wsgiref.simple_server import make_server


def application(environ, start_response):

    status = '200 OK'

    response_headers = [('Content-type', 'text/html')]

    start_response(status, response_headers)

    body = '<h1>Hello 实验楼</h1>'.encode('utf-8')

    return [body]


if __name__ == '__main__':
    # application 为一个可调用的对象
    httpd = make_server('', 8090, application)
    print("Serving HTTP on port 8090 ...")
    httpd.serve_forever()
