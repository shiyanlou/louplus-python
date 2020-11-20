import json
import redis
import gevent
from flask import Blueprint


ws = Blueprint('ws', __name__, url_prefix='/ws')
redis = redis.from_url('redis://127.0.0.1:6379')


class Chatroom(object):
    """
    聊天室，用来管理所有客户端连接
    """

    def __init__(self):
        self.clients = []
        self.pubsub = redis.pubsub()
        self.pubsub.subscribe('chat')

    def register(self, client):
        """
        注册客户端连接
        """

        self.clients.append(client)

    def unregister(self, client):
        """
        注销客户端连接
        """

        self.clients.remove(client)

    def send(self, client, data):
        """
        发送消息给某个客户端，如果失败，移除该客户端连接
        """

        try:
            client.send(data.decode('utf-8'))
        except:
            self.unregister(client)

    def run(self):
        """
        运行聊天室，监听来自订阅 channel 的消息并发送给聊天室里的所有客户端
        """

        for message in self.pubsub.listen():
            # 订阅 channel 的消息有很多种，只有 message 类型为订阅者发布
            if message['type'] == 'message':
                data = message.get('data')
                for client in self.clients:
                    gevent.spawn(self.send, client, data)

    def start(self):
        """
        使用 gevent 协程（Greenlet）来异步运行聊天室
        """

        # 为了达到更好的并发性能，协程代码需使用异步 socket
        # 可以使用 gevent.monkey 给标准 socket 打补丁来实现
        gevent.spawn(self.run)


chat = Chatroom()
chat.start()


@ws.route('/chat')
def index(ws):
    """
    WebSocket handler，使用一个 WebSocket 来同时处理数据发送和接收
    """

    # 注册 WebSocket 到聊天室
    chat.register(ws)

    # 新用户进入聊天室，发布一条提示消息
    redis.publish('chat', json.dumps(dict(
        username='New user come in, people count',
        text=len(chat.clients)
    )))

    # 如果 WebSocket 未关闭，重复进行消息接收和发送
    while not ws.closed:
        # 接收客户端消息，如果没有则阻塞在此
        message = ws.receive()
        # 客户端关闭连接时服务端会接收到一个 None 消息
        if message is None:
            break
        # 发布消息到 channel
        redis.publish('chat', message)

    # 如果 WebSocket 关闭，从聊天室里移除
    chat.unregister(ws)
