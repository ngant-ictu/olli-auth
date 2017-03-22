#!/usr/bin/python
# coding: utf-8

import jwt
import yaml
from config import default as defaultConfig

def logged_in(handler):
    """ Decorator to Authentication & Authorization using ACL """

    def check_login(self, *args, **kwargs):
        jwtToken = self.request.headers.get('Authorization', None)

        if jwtToken:
            try:
                payload = jwt.decode(
                    jwtToken,
                    defaultConfig.config['jwt_secret'],
                    algorithms=[defaultConfig.config['jwt_algorithms']],
                    issuer=defaultConfig.config['app_name']
                )

                # Authorization
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                if jwt.ExpiredSignatureError:
                    self.abort(500)  # expired
                else:
                    self.abort(400)
        else:
            self.abort(403)

        return handler(self, *args, **kwargs)
    return check_login
