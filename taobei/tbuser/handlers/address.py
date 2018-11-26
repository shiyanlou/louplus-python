from flask import Blueprint, request, current_app

from tblib.model import session
from tblib.handler import json_response, ResponseCode

from ..models import Address, AddressSchema\


address = Blueprint('address', __name__, url_prefix='/addresses')


@address.route('', methods=['POST'])
def create_address():
    data = request.get_json()

    address = AddressSchema().load(data)
    session.add(address)
    session.commit()

    return json_response(address=AddressSchema().dump(address))


@address.route('', methods=['GET'])
def address_list():
    owner_id = request.args.get('owner_id', type=int)
    order_direction = request.args.get('order_direction', 'asc')
    limit = request.args.get(
        'limit', current_app.config['PAGINATION_PER_PAGE'], type=int)
    offset = request.args.get('offset', 0, type=int)

    order_by = Address.id.asc() if order_direction == 'asc' else Address.id.desc()
    query = Address.query
    if owner_id is not None:
        query = query.filter(Address.owner_id == owner_id)
    total = query.count()
    query = query.order_by(order_by).limit(limit).offset(offset)

    return json_response(addresses=AddressSchema().dump(query, many=True), total=total)


@address.route('/<int:address_id>', methods=['POST'])
def update_address(address_id):
    data = request.get_json()

    count = Address.query.filter(
        Address.id == address_id).update(data)
    if count == 0:
        return json_response(ResponseCode.NOT_FOUND)
    address = Address.query.get(address_id)
    session.commit()

    return json_response(address=AddressSchema().dump(address))


@address.route('/<int:address_id>', methods=['GET'])
def address_info(address_id):
    address = Address.query.get(address_id)
    if address is None:
        return json_response(ResponseCode.NOT_FOUND)

    return json_response(address=AddressSchema().dump(address))
