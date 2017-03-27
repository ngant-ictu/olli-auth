#!/usr/bin/python
# coding: utf-8

import jwt
import yaml
from config import default as defaultConfig
from models.user import User as UserModel
from libs import helper as Helper

def logged_in(handler):
    """ Decorator to Authentication & Authorization using ACL """

    def check_login(self, *args, **kwargs):
        jwtToken = self.request.headers.get('Authorization', None)

        if jwtToken:
            # validate token
            try:
                userToken = jwt.decode(
                    jwtToken,
                    defaultConfig.config['jwt_secret'],
                    algorithms=[defaultConfig.config['jwt_algorithms']],
                    issuer=defaultConfig.config['app_name']
                )
            except (jwt.DecodeError, jwt.ExpiredSignatureError), e:
                self.responseJSON('TOKEN_EXPIRED', **{
                    'data': [str(e)]
                })
                return

            # check token created time and changed password time, if < -> token invalid
            try:
                myUser = UserModel.get_by_id(userToken['id'])
                assert myUser is not None
            except:
                self.responseJSON('DATA_NOTFOUND')
                return

            if myUser.date_change_password != None:
                if Helper.timestampToDatetime(userToken['iat']) < myUser.date_change_password:
                    self.responseJSON('TOKEN_INVALID_TIME')
                    return

            # check user logged out
            if myUser.status == UserModel.STATUS_LOGOUT:
                self.responseJSON('TOKEN_INVALID')
                return

            # authorization system
        else:
            self.abort(403)

        return handler(self, userToken, *args, **kwargs)
    return check_login
