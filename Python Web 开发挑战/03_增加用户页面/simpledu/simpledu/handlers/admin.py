from flask import Blueprint


admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
def index():
    """后台管理主页"""

    return 'admin'
