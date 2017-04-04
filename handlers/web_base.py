#!/usr/bin/python
# coding: utf-8
#
# Copyright @ 2017 OLLI Technologies Inc. All Rights Reserved.

""" The web base request handler class """
import webapp2
from webapp2_extras import sessions, jinja2
from libs import jinja_bootstrap

class ViewClass:
    """
        ViewClass to insert variables into the template.

        ViewClass is used in BaseHandler to promote variables automatically that can be used
        in jinja2 templates.
        Use case in a BaseHandler Class:
            self.view.var1 = "hello"
            self.view.array = [1, 2, 3]
            self.view.dict = dict(a="abc", b="bcd")
        Can be accessed in the template by just using the variables like {{var1}} or {{dict.b}}
    """
    pass

class WebHandler(webapp2.RequestHandler):
    def __init__(self, request, response):
        self.initialize(request, response)
        self.view = ViewClass()

    def render_template(self, file_name, template_args):
        self.response.headers["Cache-Control"] = "public, max-age=0"
        self.response.write(self.jinja2.render_template(file_name, **template_args))
        return None

    def dispatch(self):
        """
            Get a session store for this request.
        """
        self.session_store = sessions.get_store(request=self.request)

        try:
            # # csrf protection
            # if self.request.method == "POST":
            #     token = self.session.get('_csrf_token')
            #     if not token or (token != self.request.get('_csrf_token') and
            #              token != self.request.headers.get('_csrf_token')):
            #         self.abort(403)

            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session_store(self):
        return sessions.get_store(request=self.request)

    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()

    @webapp2.cached_property
    def messages(self):
        return self.session.get_flashes(key='_messages')

    def add_message(self, message, level=None):
        self.session.add_flash(str(message).decode('utf8'), level, key='_messages')

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(factory=jinja_bootstrap.jinja2_factory, app=self.app)

    def render_template(self, filename, **kwargs):
        # make all self.view variables available in jinja2 templates
        if hasattr(self, 'view'):
            kwargs.update(self.view.__dict__)

        # set or overwrite special vars for jinja templates
        kwargs.update({
            'url': self.request.url,
            'path': self.request.path,
            'query_string': self.request.query_string,
            'uri_for': self.uri_for,
            'session': self.session
        })

        if hasattr(self, 'form'):
            kwargs['form'] = self.form
        if self.messages:
            kwargs['messages'] = self.messages

        self.response.headers.add_header('X-UA-Compatible', 'IE=Edge,chrome=1')
        self.response.write(self.jinja2.render_template(filename, **kwargs))
