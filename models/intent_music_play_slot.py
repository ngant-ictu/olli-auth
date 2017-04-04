#!/usr/bin/python
# coding: utf-8
#
# Copyright @ 2017 OLLI Technologies Inc. All Rights Reserved.

from google.appengine.ext import ndb

class IntentMusicPlaySlot(ndb.Model):
    speech_id = ndb.IntegerProperty(required=True)
    start = ndb.IntegerProperty(required=True)
    end = ndb.IntegerProperty(required=True)
    content = ndb.StringProperty(required=True)
    type = ndb.StringProperty(required=True)
    datecreated = ndb.DateTimeProperty(auto_now_add=True)
    hltimestamp = ndb.IntegerProperty(required=True)
