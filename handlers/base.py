# *-* coding: UTF-8 *-*

import webapp2
import json
import pprint

class Debug(pprint.PrettyPrinter):
    """
        Simple print UTF8 character to debug
    """
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)

class BaseHandler(webapp2.RequestHandler):
    """
        BaseHandler for all requests

        Holds the auth and session properties so they
        are reachable for all requests
    """

    def __init__(self, request, response):
        """ Override the initialiser in order to set the language.
        """
        self.initialize(request, response)

    def dispatch(self):
        # Dispatch the request.
        webapp2.RequestHandler.dispatch(self)

    def responseJSON(self, **kwargs):
        self.response.headers['Content-Type'] = 'text/json'
        self.response.out.write(json.dumps(kwargs).encode('utf-8'))
        return

    def debug(self, output):
        return Debug().pprint(output)
