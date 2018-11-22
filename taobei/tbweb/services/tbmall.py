from random import choice

from tblib.service import Service


class TbMall(Service):
    @property
    def base_url(self):
        return choice(self.app.config['SERVICE_TBMALL']['addresses'])
