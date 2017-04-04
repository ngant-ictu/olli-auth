#!/usr/bin/python
# coding: utf-8
#
# Copyright @ 2017 OLLI Technologies Inc. All Rights Reserved.

from google.appengine.ext import ndb

class IntentSpeech(ndb.Model):
    content = ndb.StringProperty(required=True)
    intent = ndb.StringProperty(required=True)
    datecreated = ndb.DateTimeProperty(auto_now_add=True)
