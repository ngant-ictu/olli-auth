#!/usr/bin/python
# coding: utf-8

import jwt
import yaml
from config import default as defaultConfig
from models.user import User as UserModel
from libs import helper as Helper
from google.appengine.api import users

def logged_in(handler):
    """ Decorator to Authentication & Authorization using ACL via RESTFUL api """

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

def web_user_required(handler):
    """ Decorator to Authentication via google account """

    def web_auth_required(self, *args, **kwargs):
        if (users.get_current_user() or self.request.headers.get('X-AppEngine-Cron')):
            handler(self, *args, **kwargs)
        else:
            self.redirect(users.create_login_url(dest_url=str(self.request.path)))
    return web_auth_required

def web_admin_required(handler):
    """
         Decorator for checking if there's a admin user associated
         with the current session.
         Will also fail if there's no session present.
    """

    def check_admin(self, *args, **kwargs):
        """
            If handler has no login_url specified invoke a 403 error
        """
        if not users.is_current_user_admin():
            self.response.write(
                '<div style="padding-top: 200px; height:178px; width: 500px; color: white; margin: 0 auto; font-size: 52px; text-align: center; background: url(\'http://3.bp.blogspot.com/_d_q1e2dFExM/TNWbWrJJ7xI/AAAAAAAAAjU/JnjBiTSA1xg/s1600/Bank+Vault.jpg\')">Forbidden Access <a style=\'color: white;\' href=\'%s\'>Login</a></div>' %
                users.create_login_url(self.request.path_url + self.request.query_string))
            return
        else:
            return handler(self, *args, **kwargs)

    return check_admin
