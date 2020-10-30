""" rmon.views.urls

定义了所有 API 对应的 URL
"""
from flask import Blueprint

from rmon.views.index import IndexView
from rmon.views.server import (ServerCommand, ServerDetail, ServerList,
                               ServerMetrics)
from rmon.views.user import UserList, UserDetail
from rmon.views.auth import AuthView, RefreshTokenView
from rmon.views.wx import WxView, WxBind

api = Blueprint('api', __name__)

# 首页
api.add_url_rule('/', view_func=IndexView.as_view('index'))

# 登录
api.add_url_rule('/login', view_func=AuthView.as_view('login'))
api.add_url_rule('/token/refresh',
                 view_func=RefreshTokenView.as_view('refresh_token'))

# 用户管理
api.add_url_rule('/users/', view_func=UserList.as_view('user_list'))
api.add_url_rule('/users/<int:object_id>',
                 view_func=UserDetail.as_view('user_detail'))

# Redis 服务器管理
api.add_url_rule('/servers/',
                 view_func=ServerList.as_view('server_list'))
api.add_url_rule('/servers/<int:object_id>',
                 view_func=ServerDetail.as_view('server_detail'))
api.add_url_rule('/servers/<int:object_id>/metrics',
                 view_func=ServerMetrics.as_view('server_metrics'))
api.add_url_rule('/servers/<int:object_id>/command',
                 view_func=ServerCommand.as_view('server_command'))

# 微信接口
api.add_url_rule('/wx/', view_func=WxView.as_view('wx_view'))
api.add_url_rule('/wx/bind/<wx_id>', view_func=WxBind.as_view('wx_bind'))
