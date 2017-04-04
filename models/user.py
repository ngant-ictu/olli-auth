#!/usr/bin/python
# coding: utf-8

from google.appengine.ext import ndb

class User(ndb.Model):
    email = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    groupid = ndb.IntegerProperty(required=True)
    status = ndb.IntegerProperty(required=True)
    code_activation = ndb.StringProperty(required=True)
    date_created = ndb.DateTimeProperty(auto_now_add=True)
    date_modified = ndb.DateTimeProperty(auto_now=True)
    date_change_password = ndb.DateTimeProperty()
    date_forgot_password = ndb.DateTimeProperty()
    date_activation = ndb.DateTimeProperty()

    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 3
    STATUS_LOGOUT = 5
