from flask import abort
from flask_login import current_user
from functools import wraps
from simpledu.models import User


def role_required(role):
    """ 该装饰器假定用户已经登录了，所以应该用在 login_required 之上
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwrargs):
            if current_user.role < role:
                abort(404)
            return func(*args, **kwrargs)
        return wrapper
    return decorator


staff_required = role_required(User.ROLE_STAFF)
admin_required = role_required(User.ROLE_ADMIN)
