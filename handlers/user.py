from handlers.base import BaseHandler
from libs.decorators import logged_in

class ListHandler(BaseHandler):

    @logged_in
    def get(self):
        params = {
            'id': 1
        }

        self.debug(params)
        self.responseJSON(**params)
