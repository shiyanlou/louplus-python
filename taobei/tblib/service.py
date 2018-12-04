from random import choice

import requests


class ServiceResponseNotOk(Exception):
    pass


class Service(requests.Session):
    def __init__(self, app, timeout=5):
        super().__init__()

        self.app = app
        self.timeout = timeout

    @property
    def base_url(self):
        """服务基本地址，包括协议、域名和可选的路径前缀，子类需要覆盖实现该方法
        """

        return ''

    def check_code(self, json):
        if json['code'] != 0:
            raise ServiceResponseNotOk(
                '{}: {}'.format(json['code'], json['message']))

    def get(self, path, **kwargs):
        url = self.base_url + path
        kwargs.setdefault('timeout', self.timeout)
        return super().get(url, **kwargs)

    def get_json(self, path, check_code=True, **kwargs):
        resp = self.get(path, **kwargs)

        json = resp.json()

        if check_code:
            self.check_code(json)

        return json

    def post(self, path, data=None, json=None, **kwargs):
        url = self.base_url + path
        kwargs.setdefault('timeout', self.timeout)
        return super().post(url, data, json, **kwargs)

    def post_json(self, path, data=None, json=None, check_code=True,
                  filter_none_field=True, **kwargs):
        if isinstance(data, dict) and filter_none_field:
            data = {k: v for k, v in data.items() if v is not None}
        if isinstance(json, dict) and filter_none_field:
            json = {k: v for k, v in json.items() if v is not None}

        resp = self.post(path, data, json, **kwargs)

        json = resp.json()

        if check_code:
            self.check_code(json)

        return json

    def delete(self, path, **kwargs):
        url = self.base_url + path
        kwargs.setdefault('timeout', self.timeout)
        return super().delete(url, **kwargs)

    def delete_json(self, path, check_code=True, **kwargs):
        resp = self.delete(path, **kwargs)

        json = resp.json()

        if check_code:
            self.check_code(json)

        return json
