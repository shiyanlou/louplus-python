from tblib.handler import handle_error_json

from .file import file


def init(app):
    app.register_error_handler(Exception, handle_error_json)

    app.register_blueprint(file)
