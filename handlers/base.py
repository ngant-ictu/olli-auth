#!/usr/bin/python
# coding: utf-8

import os
import webapp2
import json
import pprint
from config import errorcode as ErrorCode
from collections import OrderedDict

class Debug(pprint.PrettyPrinter):
    """
        Simple print UTF8 character to debug
    """
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
            import pdb; pdb.set_trace();
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
        """ Prepare to dispatch request """

        # Dispatch the request.
        webapp2.RequestHandler.dispatch(self)

    def responseJSON(self, errorConstant, **kwargs):
        """ Custom Response data to client """

        output = OrderedDict()
        self.response.headers['Content-Type'] = 'text/json; charset=utf-8'

        if len(errorConstant) > 0:
            output = ErrorCode.error[errorConstant]

            try:
                kwargs['data']
            except:
                pass
            else:
                output['data'] = []
                for msg in kwargs['data']:
                    output['data'].append(msg)

            self.response.status_int = ErrorCode.error[errorConstant]['status_code']

            if os.environ['SERVER_SOFTWARE'].startswith('Dev') == False:
                del ErrorCode.error[errorConstant]['dev_message']

            return self.response.out.write(json.dumps(output).encode('utf-8'))
        else:
            kwargs['status_code'] = 200
            return self.response.out.write(json.dumps(kwargs).encode('utf-8'))

    def debug(self, output):
        """ Simple function to beauty print output in console """

        return Debug().pprint(output)

    def parseBody(self, requestBody):
        """ Parse request body from raw json data request """

        return json.loads(requestBody)

    def getHostname(self):
        return self.request.host_url
