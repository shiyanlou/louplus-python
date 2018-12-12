from random import choice

from tblib.service import Service


class TbUser(Service):
    @property
    def base_url(self):
        return choice(self.app.config['SERVICE_TBUSER']['addresses'])
