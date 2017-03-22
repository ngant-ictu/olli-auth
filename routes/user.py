#!/usr/bin/python
# coding: utf-8

from webapp2_extras.routes import RedirectRoute
from handlers import user

secure_scheme = 'https'

_routes = [
    RedirectRoute('/api/users', user.ListHandler, name='user-list', strict_slash=True, methods=['GET']),
    # RedirectRoute('/api/users/<id>', user.ProfileHandler, name='user-profile', strict_slash=True, methods=['GET', 'POST', 'PUT', 'DELETE']),
    # # RedirectRoute('/api/user', user.CreateHandler, name='user-create', strict_slash=True, methods=['POST']),
    RedirectRoute('/api/user/register', user.RegisterHandler, name='user-register', strict_slash=True, methods=['POST']),
    RedirectRoute('/api/user/login/email', user.EmailLoginHandler, name='user-email-login', strict_slash=True, methods=['POST']),
    # RedirectRoute('/api/logout', user.LogoutHandler, name='user-logout', strict_slash=True)
]

def get_routes():
    return _routes

def add(app):
    if app.debug:
        secure_scheme = 'http'
    for r in _routes:
        app.router.add(r)
