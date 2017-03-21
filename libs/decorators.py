# *-* coding: UTF-8 *-*

import jwt
from config import default as defaultConfig

def logged_in(handler):
    def check_login(self, *args, **kwargs):
        jwtToken = self.request.headers.get('Authorization', None)

        if jwtToken:
            try:
                payload = jwt.decode(jwtToken, 'secret', algorithms=['HS256'])
                print payload
            except (AttributeError, KeyError), e:
                print e
        else:
            self.abort(403)
            
        # if self.request.query_string != '':
        #     query_string = '?' + self.request.query_string
        # else:
        #     query_string = ''
        #
        # continue_url = self.request.path_url + query_string
        # login_url = self.uri_for('login', **{'continue': continue_url})
        #
        # try:
        #     auth_token = self.session.get("auth_token")
        #
        #     if auth_token == None:
        #         try:
        #             self.redirect(login_url, abort=True)
        #         except (AttributeError, KeyError), e:
        #             self.abort(403)
        #     else:
        #         auth_role = self.session.get("auth_role")
        #         if auth_role != 1:
        #             self.abort(403)
        #
        # except AttributeError, e:
        # # 	# avoid AttributeError when the session was delete from the server
        # # 	logging.error(e)
        #     self.auth.unset_session()
        #     self.redirect(login_url)

        return handler(self, *args, **kwargs)
    return check_login
