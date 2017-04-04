#!/usr/bin/python
# coding: utf-8

from webapp2_extras.routes import RedirectRoute
from handlers import annotation

secure_scheme = 'https'

_routes = [
    RedirectRoute('/admin/annotation', annotation.ListHandler, name='annotation-list', strict_slash=True),
    RedirectRoute('/admin/annotation/createsample', annotation.AnnotationSampleHandler, name='annotation-create-sample', strict_slash=True),
    RedirectRoute('/admin/annotation/createslot', annotation.SlotCreateHandler, name='annotation-create-slot', strict_slash=True),
    RedirectRoute('/admin/annotation/deleteslot', annotation.SlotDeleteHandler, name='annotation-delete-slot', strict_slash=True),
    RedirectRoute('/admin/annotation/deletespeech', annotation.SpeechDeleteHandler, name='annotation-delete-speech', strict_slash=True),
    RedirectRoute('/admin/annotation/resetspeech', annotation.SpeechResetHandler, name='annotation-reset-speech', strict_slash=True),
]

def get_routes():
    return _routes

def add(app):
    if app.debug:
        secure_scheme = 'http'
    for r in _routes:
        app.router.add(r)
