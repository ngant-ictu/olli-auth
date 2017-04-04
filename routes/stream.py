#!/usr/bin/python
# coding: utf-8

from webapp2_extras.routes import RedirectRoute
from handlers import stream

secure_scheme = 'https'

_routes = [
    RedirectRoute('/', stream.MainHandler, name='stream-main', strict_slash=True)
]

def get_routes():
    return _routes

def add(app):
    if app.debug:
        secure_scheme = 'http'
    for r in _routes:
        app.router.add(r)
