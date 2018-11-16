from flask import Blueprint, request, current_app

from ..db import session
from ..models import Address, AddressSchema
from .common import json_response, ResponseCode


address = Blueprint('address', __name__, url_prefix='/')


@address.route('/addresses', methods=['POST'])
def create_address():
    address = AddressSchema().load(request.get_json())

    session.add(address)
    session.commit()

    return json_response(address=AddressSchema().dump(address))


@address.route('/addresses', methods=['GET'])
def address_list():
    limit = request.args.get(
        'limit', current_app.config['FLASK_SQLALCHEMY_PER_PAGE'], type=int)
    offset = request.args.get('offset', 0, type=int)

    query = session.query(Address).limit(limit).offset(offset)

    return json_response(addresses=AddressSchema().dump(query.all(), many=True))


@address.route('/addresses/<int:address_id>', methods=['POST'])
def update_address(address_id):
    values = request.get_json()

    count = session.query(Address).filter(
        Address.id == address_id).update(values)
    if count == 0:
        return json_response(ResponseCode.NOT_FOUND)
    address = session.query(Address).get(address_id)
    session.commit()

    return json_response(address=AddressSchema().dump(address))


@address.route('/addresses/<int:address_id>', methods=['GET'])
def address_info(address_id):
    address = session.query(Address).get(address_id)
    if address is None:
        return json_response(ResponseCode.NOT_FOUND)

    return json_response(address=AddressSchema().dump(address))
