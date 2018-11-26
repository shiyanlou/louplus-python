from tblib.handler import handle_error

from .file import file


def init(app):
    app.register_error_handler(Exception, handle_error)

    app.register_blueprint(file)
