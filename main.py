#!/usr/bin/env python
# *-* coding: UTF-8 *-*

import os
import sys
import json

# Third party libraries path must be fixed before importing webapp2
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'libs/external'))

import webapp2

from config import default as defaultConfig
from routes import user as userRoutes

webapp2Config = defaultConfig.config

# Error handle
def handle_400(request, response, exception):
    response.headers['Content-Type'] = 'text/json'
    response.out.write(json.dumps({
        'code': 400,
        'message': str(exception)
    }).encode('utf-8'))
    response.set_status(400)

def handle_404(request, response, exception):
    response.headers['Content-Type'] = 'text/json'
    response.out.write(json.dumps({
        'code': 404,
        'message': str(exception)
    }).encode('utf-8'))
    response.set_status(404)

def handle_500(request, response, exception):
    response.headers['Content-Type'] = 'text/json'
    response.out.write(json.dumps({
        'code': 500,
        'message': str(exception)
    }).encode('utf-8'))
    response.set_status(500)
    print exception

def handle_405(request, response, exception):
    response.headers['Content-Type'] = 'text/json'
    response.out.write(json.dumps({
        'code': 405,
        'message': str(exception)
    }).encode('utf-8'))
    response.set_status(405)

def handle_403(request, response, exception):
    response.headers['Content-Type'] = 'text/json'
    response.out.write(json.dumps({
        'code': 403,
        'message': str(exception)
    }).encode('utf-8'))
    response.set_status(403)

app = webapp2.WSGIApplication(debug=os.environ['SERVER_SOFTWARE'].startswith('Dev'), config=webapp2Config)

# Routes add
userRoutes.add(app)

app.error_handlers[400] = handle_400
app.error_handlers[403] = handle_403
app.error_handlers[404] = handle_404
app.error_handlers[405] = handle_405
app.error_handlers[500] = handle_500
