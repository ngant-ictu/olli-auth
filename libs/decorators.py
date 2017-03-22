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
                    jwtToken, defaultConfig.config['secret_key'],
                    algorithms=[defaultConfig.config['algorithms']]
                )

                # Authorization
            except AttributeError, e:
                self.abort(500)
        else:
            self.abort(403)

        return handler(self, *args, **kwargs)
    return check_login
