import traceback

from flask import jsonify


class ResponseCode:
    OK = 0
    ERROR = 1
    NOT_FOUND = 10
    TRANSACTION_FAILURE = 20
    QUANTITY_EXCEEDS_LIMIT = 30
    NO_ENOUGH_MONEY = 40

    MESSAGES = {
        OK: '成功',
        ERROR: '未知错误',
        NOT_FOUND: '资源未找到',
        TRANSACTION_FAILURE: '执行事务失败',
        QUANTITY_EXCEEDS_LIMIT: '数量超过限制',
        NO_ENOUGH_MONEY: '余额不足',
    }


def json_response(code=ResponseCode.OK, message='', **kwargs):
    return jsonify({
        'code': code,
        'message': message or ResponseCode.MESSAGES.get(code, ''),
        'data': kwargs
    })


def handle_error_json(exception):
    traceback.print_exc()

    return json_response(ResponseCode.ERROR, str(exception))
