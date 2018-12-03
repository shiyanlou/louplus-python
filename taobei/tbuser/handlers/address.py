from flask import Blueprint, request, current_app
from werkzeug.exceptions import BadRequest

from tblib.model import session
from tblib.handler import json_response, ResponseCode

from ..models import Address, AddressSchema\


address = Blueprint('address', __name__, url_prefix='/addresses')


@address.route('', methods=['POST'])
def create_address():
    """添加地址
    """

    data = request.get_json()

    address = AddressSchema().load(data)
    session.add(address)
    session.commit()

    return json_response(address=AddressSchema().dump(address))


@address.route('', methods=['GET'])
def address_list():
    """查询地址列表，可通过用户 ID 等字段筛选
    """

    user_id = request.args.get('user_id', type=int)
    order_direction = request.args.get('order_direction', 'desc')
    limit = request.args.get(
        'limit', current_app.config['PAGINATION_PER_PAGE'], type=int)
    offset = request.args.get('offset', 0, type=int)

    order_by = Address.id.asc() if order_direction == 'asc' else Address.id.desc()
    query = Address.query
    if user_id is not None:
        query = query.filter(Address.user_id == user_id)
    total = query.count()
    query = query.order_by(order_by).limit(limit).offset(offset)

    return json_response(addresses=AddressSchema().dump(query, many=True), total=total)


@address.route('/<int:id>', methods=['POST'])
def update_address(id):
    """更新地址
    """

    data = request.get_json()

    if data.get('is_default'):
        Address.query.filter(Address.is_default == True).update({
            'is_default': False,
        })

    count = Address.query.filter(
        Address.id == id).update(data)
    if count == 0:
        return json_response(ResponseCode.NOT_FOUND)
    address = Address.query.get(id)
    session.commit()

    return json_response(address=AddressSchema().dump(address))


@address.route('/<int:id>', methods=['GET'])
def address_info(id):
    """查询地址
    """

    address = Address.query.get(id)
    if address is None:
        return json_response(ResponseCode.NOT_FOUND)

    return json_response(address=AddressSchema().dump(address))


@address.route('/infos', methods=['GET'])
def address_infos():
    """批量查询用户，查询指定 ID 列表里的多个地址
    """

    ids = []
    for v in request.args.get('ids', '').split(','):
        id = int(v.strip())
        if id > 0:
            ids.append(id)
    if len(ids) == 0:
        raise BadRequest()

    query = Address.query.filter(Address.id.in_(ids))

    addresses = {address.id: AddressSchema().dump(address)
                 for address in query}

    return json_response(addresses=addresses)
