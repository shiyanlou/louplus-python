import re
import os
from wechatpy.messages import TextMessage
from wechatpy import create_reply
from qqwry import QQwry

class CommandHandler:
    command = ''

    def check_match(self, message):
        """检查消息是否匹配命令模式
        """
        if not isinstance(message, TextMessage):
            return False
        if not message.content.strip().lower().startswith(self.command):
            return False
        return True


class IPLocationHandler(CommandHandler):
    command = 'ip'

    def __init__(self):
        file = os.environ.get('QQWRY_DAT', 'qqwry.dat')
        self.q = QQwry()
        self.q.load_file(file)

    def handle(self, message):
        if not self.check_match(message):
            return
        parts = message.content.strip().split()
        if len(parts) == 1 or len(parts) > 2:
            return create_reply('IP地址无效', message)
        ip = parts[1]
        pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
        if not re.match(pattern, ip):
            return create_reply('IP地址无效', message)
        result = self.q.lookup(ip)
        if result is None:
            return create_reply('未找到', message)
        else:
            return create_reply(result[0], message)
