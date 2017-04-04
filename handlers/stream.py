#!/usr/bin/python
# coding: utf-8

from handlers.web_base import WebHandler
from libs.decorators import web_user_required
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

class MainHandler(WebHandler):
    """
        Stream record demo
    """
    @web_user_required
    def get(self):
        template_args = {}
        return self.render_template('stream/main.html', **template_args)
