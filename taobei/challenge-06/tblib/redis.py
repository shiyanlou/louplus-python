from flask_redis import FlaskRedis

redis = FlaskRedis()


def init(app):
    global redis

    redis.init_app(app)
