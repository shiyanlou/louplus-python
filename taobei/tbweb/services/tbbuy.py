from random import choice

from tblib.service import Service


class TbBuy(Service):
    @property
    def base_url(self):
        return choice(self.app.config['SERVICE_TBBUY']['addresses'])
