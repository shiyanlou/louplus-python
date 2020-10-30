import os
import json
from flask import Flask


def create_app():
    app = Flask('rmon')
    file = os.environ.get('RMON_CONFIG')
    content =''
    try:
        with open(file) as f:
            for l in f:
                l = l.strip()
                if l.startswith('#'):
                    continue
                else:
                    content += l
    except IOError:
        return app

    try:
        data = json.loads(content)
    except:
        return app

    for key in data:
        app.config[key.upper()] = data.get(key)
    return app
