#!/usr/bin/python
# coding: utf-8

import re
import os
import hashlib
from pbkdf2 import crypt
from config import default as defaultConfig
from datetime import datetime, timedelta
import time
import jwt

def hash_password(pwraw):
    """ Hash a unique email and password of user """

    hashCrypt = crypt(pwraw, defaultConfig.config['salt'], iterations=567)
    h = hashlib.md5()
    h.update(hashCrypt)
    return h.hexdigest()

def emailValid(emailAddress):
    """ Check valid email address """

    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', emailAddress)
    if match == None:
        return False
    else:
        return True

def createToken(payload):
    """ Create JWT Token """

    payload['exp'] = datetime.utcnow() + timedelta(seconds=defaultConfig.config['jwt_expire'])
    payload['iss'] = defaultConfig.config['app_name']
    payload['iat'] = datetime.utcnow()
    return jwt.encode(payload, defaultConfig.config['jwt_secret'], defaultConfig.config['jwt_algorithms'])

def datetimeToTimestamp(dateTimeObject):
    """ Convert from Datetime to Timestamp """

    return time.mktime(dateTimeObject.timetuple())

def timestampToDatetime(timestampValue):
    """ Convert from Timestamp to Datetime """

    return datetime.fromtimestamp(timestampValue)
