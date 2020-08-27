import sys, socket

def scan():
    args = sys.argv
    try:
        host = args[args.index('--host')+1]
        port = args[args.index('--port')+1]
        assert len(host.split('.')) == 4
        if '-' in port:
            start, end = port.split('-')
            assert int(start) < int(end)
            ports = range(int(start), int(end)+1)
        else:
            ports = [int(port)]
    except (ValueError, IndexError, AssertionError):
        print('Parameter Error')
        exit()

    open_ports = []
    s = socket.socket()     # 创建套接字
    s.settimeout(0.1)       # 设置套接字操作的超时期，参数为浮点数，单位是秒

    for port in ports:
        # connect 方法的作用是初始化 TCP 服务器连接
        # connect_ex 是 connect 的扩展版本，接收主机＋端口号元组作为参数
        # 出错时返回出错码，而不是抛出异常，出错码是非零数字
        if s.connect_ex((host, port)) == 0:
            open_ports.append(port)
            print(port, 'open')
        else:
            print(port, 'close')

    s.close()
    print('Complted scan. Opening ports at {}'.format(open_ports))

if __name__ == '__main__':
    scan()
