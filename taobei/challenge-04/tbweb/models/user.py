from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user):
        self.id = user.get('id')
        self.username = user.get('username')
        self.avatar = user.get('avatar')
        self.mobile = user.get('mobile')
        self.gender = user.get('gender')
        self.wallet_money = user.get('wallet_money')
        self.created_at = user.get('created_at')
        self.updated_at = user.get('updated_at')
