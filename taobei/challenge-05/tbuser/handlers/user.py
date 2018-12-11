from flask import Blueprint, request, current_app
from sqlalchemy import or_
from werkzeug.exceptions import BadRequest

from tblib.model import session
from tblib.handler import json_response, ResponseCode

from ..models import User, UserSchema, User, UserSchema, WalletTransaction, WalletTransactionSchema

user = Blueprint('user', __name__, url_prefix='/users')


@user.route('', methods=['POST'])
def create_user():
    """注册用户
    """

    data = request.get_json()
    password = data.pop('password')

    user = UserSchema().load(data)
    user.password = password
    session.add(user)
    session.commit()

    return json_response(user=UserSchema().dump(user))


@user.route('', methods=['GET'])
def user_list():
    """查询用户列表，可通过用户名、手机等字段进行筛选
    """

    username = request.args.get('username')
    mobile = request.args.get('mobile')
    order_direction = request.args.get('order_direction', 'desc')
    limit = request.args.get(
        'limit', current_app.config['PAGINATION_PER_PAGE'], type=int)
    offset = request.args.get('offset', 0, type=int)

    order_by = User.id.asc() if order_direction == 'asc' else User.id.desc()
    query = User.query
    if username is not None:
        query = query.filter(User.username == username)
    if mobile is not None:
        query = query.filter(User.mobile == mobile)
    total = query.count()
    query = query.order_by(order_by).limit(limit).offset(offset)

    return json_response(users=UserSchema().dump(query, many=True), total=total)


@user.route('/<int:id>', methods=['POST'])
def update_user(id):
    """更新用户
    """

    data = request.get_json()

    user = User.query.get(id)
    if user is None:
        return json_response(ResponseCode.NOT_FOUND)
    for key, value in data.items():
        setattr(user, key, value)
    session.commit()

    return json_response(user=UserSchema().dump(user))


@user.route('/<int:id>', methods=['GET'])
def user_info(id):
    """查询用户
    """

    user = User.query.get(id)
    if user is None:
        return json_response(ResponseCode.NOT_FOUND)

    return json_response(user=UserSchema().dump(user))


@user.route('/infos', methods=['GET'])
def user_infos():
    """批量查询用户，查询指定 ID 列表里的多个用户
    """

    ids = []
    for v in request.args.get('ids', '').split(','):
        id = int(v.strip())
        if id > 0:
            ids.append(id)
    if len(ids) == 0:
        raise BadRequest()

    query = User.query.filter(User.id.in_(ids))

    users = {user.id: UserSchema().dump(user)
             for user in query}

    return json_response(users=users)


@user.route('/check_password', methods=['GET'])
def check_password():
    """验证用户名和密码是否匹配
    """

    username = request.args.get('username')
    password = request.args.get('password')
    if username is None or password is None:
        return json_response(isCorrect=False)

    user = User.query.filter(User.username == username).first()
    if user is None:
        return json_response(isCorrect=False)

    isCorrect = user.check_password(password)

    return json_response(isCorrect=isCorrect, user=UserSchema().dump(user) if isCorrect else None)
