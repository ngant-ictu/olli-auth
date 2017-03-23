#!/usr/bin/python
# coding: utf-8

from google.appengine.ext import ndb

class InvalidToken(ndb.Model):
    token = ndb.StringProperty(required=True)
