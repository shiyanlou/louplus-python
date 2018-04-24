import socket
import io
import sys

from app import Flask


class WSGIServer:

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 1

    def __init__(self, addr, port):

        # 创建socket，利用socket获取客户端的请求
        self.listen_socket = listen_socket = socket.socket(self.address_family, self.socket_type)
        # 设置socket的工作模式
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 绑定 socket 地址
        listen_socket.bind((addr, port))
        # socket active， 监听文件描述符
        listen_socket.listen(self.request_queue_size)

        # 获得 server 的 hostname 和port
        host, port = self.listen_socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port

        self.headers = []

    def set_app(self, application):
        self.application = application

    def serve_forever(self):
        """ 启动 WSGI server 获取链接
        """
        listen_socket = self.listen_socket
        while True:
            # 接受客户端请求
            conn, client_info = listen_socket.accept()
            print(client_info)
            print('receive request from %s:%d' % (client_info[0], client_info[1]))
            # 处理请求
            self.handle_one_request(conn)

    def handle_one_request(self, conn):
        """ 处理请求
        """
        request_data = conn.recv(1024)
        http_method, path, request_version = self.parse_request(request_data)
        # print(''.join(
        # '< {line}\n'.format(line=line)
        # for line in request_data.splitlines()
        # ))
        # Construct environment dictionary using request data
        env = self.get_environ(http_method, path, request_data)

        #给flask\tornado传递两个参数，environ，start_response
        result = self.application(env, self.start_response)
        self.finish_response(conn, result)

    def parse_request(self, data):
        """ 解析 HTTP 请求
        """
        format_data = data.splitlines()
        if len(format_data):
            request_line = data.splitlines()[0]
            request_line = request_line.rstrip(b'\r\n')
            # ['GET', '/', 'HTTP/1.1']
            return str(request_line).split()

    def get_environ(self, method, path, data):
        """ 获取环境
        """
        # 获取environ数据并设置当前 Server 的工作模式
        env = {}
        env['wsgi.version']      = (1, 0)
        env['wsgi.url_scheme']   = 'http'
        env['wsgi.input']        = io.BytesIO(data)
        env['wsgi.errors']       = sys.stderr
        env['wsgi.multithread']  = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once']     = False
        # Required CGI variables
        env['REQUEST_METHOD']    = method
        env['PATH_INFO']         = path
        env['SERVER_NAME']       = self.server_name
        env['SERVER_PORT']       = str(self.server_port)
        return env

    def start_response(self, status, response_headers, exc_info=None):
        """ 开始处理请求
        """
        # server_headers = [('Date', 'Tue, 31 Mar 2015 12:54:48 GMT'), ('Server', 'louplus-python-server 1.0')]
        self.headers = [status, response_headers]

    def finish_response(self, conn, result):
        """
        把 application 返回给WSGI的数据返回给客户端。
        """
        try:
            status, response_headers = self.headers
            response = 'HTTP/1.1 {status}\r\n'.format(status=status)
            for header in response_headers:
                response += '{0}: {1}\r\n'.format(*header)
            response += '\r\n'
            for data in result:
                response += data.decode('utf-8')
            conn.sendall(response.encode('utf8'))
            print(''.join('> {line}\n'.format(line=line) for line in response.splitlines()))
        finally:
            conn.close()


if __name__ == '__main__':

    server = WSGIServer('', 8093)

    app = Flask()
    server.set_app(app)
    print('Serving HTTP on port 8093 ...')
    server.serve_forever()
