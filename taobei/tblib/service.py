from random import choice

import requests


class ServiceResponseNotOk(Exception):
    pass


class Service(requests.Session):
    def __init__(self, app):
        super().__init__()

        self.app = app

    @property
    def base_url(self):
        return ''

    def get(self, path, **kwargs):
        url = self.base_url + path
        return super().get(url, **kwargs)

    def get_json(self, path, check_code=True, **kwargs):
        resp = self.get(path, **kwargs)
        json = resp.json()
        if check_code and json['code'] != 0:
            raise ServiceResponseNotOk(
                '{}: {}'.format(json['code'], json['message']))
        return json

    def post(self, path, data=None, json=None, **kwargs):
        url = self.base_url + path
        return super().post(url, data, json, **kwargs)

    def post_json(self, path, json, check_code=True, **kwargs):
        resp = self.post(path, json=json, **kwargs)
        json = resp.json()
        if check_code and json['code'] != 0:
            raise ServiceResponseNotOk(
                '{}: {}'.format(json['code'], json['message']))
        return json
