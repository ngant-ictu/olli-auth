#!/usr/bin/python
# coding: utf-8

from google.appengine.ext import ndb

class User(ndb.Model):
    email = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    groupid = ndb.IntegerProperty(required=True)
    datecreated = ndb.DateTimeProperty(auto_now_add=True)
    datemodified = ndb.DateTimeProperty(auto_now=True)
    datechangepassword = ndb.DateTimeProperty()
