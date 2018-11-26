import traceback

from flask import jsonify
from werkzeug.exceptions import HTTPException, NotFound


class ResponseCode:
    UNKNOWN_ERROR = -1
    OK = 0
    HTTP_EXCEPTION = 1
    NOT_FOUND = 10
    TRANSACTION_FAILURE = 20

    MESSAGES = {
        UNKNOWN_ERROR: '未知错误',
        OK: '成功',
        HTTP_EXCEPTION: 'HTTP 错误',
        NOT_FOUND: '资源未找到',
        TRANSACTION_FAILURE: '执行事务失败',
    }


def json_response(code=ResponseCode.OK, message='', **kwargs):
    return jsonify({
        'code': code,
        'message': message or ResponseCode.MESSAGES.get(code, ''),
        'data': kwargs
    })


def handle_error(exception):
    traceback.print_exc()

    code = ResponseCode.UNKNOWN_ERROR
    if isinstance(exception, NotFound):
        code = ResponseCode.NOT_FOUND
    elif isinstance(exception, HTTPException):
        code = ResponseCode.HTTP_EXCEPTION
    return json_response(code, exception=str(exception))
