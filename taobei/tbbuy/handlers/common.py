from flask import jsonify


class ResponseCode:
    UNKNOWN = -1
    OK = 0
    NOT_FOUND = 1

    MESSAGES = {
        UNKNOWN: '未知错误',
        OK: '成功',
        NOT_FOUND: '资源未找到',
    }


def json_response(code=ResponseCode.OK, message='', **kwargs):
    return jsonify({
        'code': code,
        'message': message or ResponseCode.MESSAGES.get(code, ''),
        'data': kwargs
    })


def handle_error(e):
    return json_response(ResponseCode.UNKNOWN, str(e))
