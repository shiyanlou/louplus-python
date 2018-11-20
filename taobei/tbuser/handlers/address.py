from flask import Blueprint, request, current_app

from ..db import session
from ..models import Address, AddressSchema
from .common import json_response, ResponseCode


address = Blueprint('address', __name__, url_prefix='/')


@address.route('/addresses', methods=['POST'])
def create_address():
    data = request.get_json()

    address = AddressSchema().load(data)
    session.add(address)
    session.commit()

    return json_response(address=AddressSchema().dump(address))


@address.route('/addresses', methods=['GET'])
def address_list():
    order_direction = request.args.get('order_direction', 'asc')
    limit = request.args.get(
        'limit', current_app.config['FLASK_SQLALCHEMY_PER_PAGE'], type=int)
    offset = request.args.get('offset', 0, type=int)

    order_by = Address.id.asc() if order_direction == 'asc' else Address.id.desc()
    query = Address.query.order_by(order_by).limit(limit).offset(offset)

    return json_response(addresses=AddressSchema().dump(query, many=True))


@address.route('/addresses/<int:address_id>', methods=['POST'])
def update_address(address_id):
    data = request.get_json()

    count = Address.query.filter(
        Address.id == address_id).update(data)
    if count == 0:
        return json_response(ResponseCode.NOT_FOUND)
    address = Address.query.get(address_id)
    session.commit()

    return json_response(address=AddressSchema().dump(address))


@address.route('/addresses/<int:address_id>', methods=['GET'])
def address_info(address_id):
    address = Address.query.get(address_id)
    if address is None:
        return json_response(ResponseCode.NOT_FOUND)

    return json_response(address=AddressSchema().dump(address))
