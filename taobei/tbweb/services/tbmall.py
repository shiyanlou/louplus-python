from random import choice

import requests


class TbMall(requests.Session):
    def __init__(self, app):
        super().__init__()

        self.app = app

    @property
    def base_url(self):
        return choice(self.app.config['SERVICE_TBMALL']['addresses'])

    def get(self, path, **kwargs):
        url = self.base_url + path
        return super().get(url, **kwargs)

    def post(self, path, data=None, json=None, **kwargs):
        url = self.base_url + path
        return super().post(url, data, json, **kwargs)
