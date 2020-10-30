from flask import Flask, render_template
from .handlers import job

def create_app(config):
    app = Flask(__name__)
    app.config['FLASK_ENV'] = config
    app.register_blueprint(job)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/g2')
    def g2():
        return render_template('g2.html')

    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    return app
