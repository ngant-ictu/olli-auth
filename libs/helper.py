#!/usr/bin/python
# coding: utf-8

import re
import os
import hashlib
import httplib2
import urllib
import time
import jwt
import string
import random
from pbkdf2 import crypt
from config import default as defaultConfig
from datetime import datetime, timedelta

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

def send_mail(htmlMessage, subject, recipient):
    """ Send email using Mailgun """

    http = httplib2.Http()
    http.add_credentials('api', defaultConfig.config['mailgun_api_key'])
    url = defaultConfig.config['mailgun_url'].format(defaultConfig.config['mailgun_domain'])

    data = {
        'from': defaultConfig.config['mailgun_sender'].format(defaultConfig.config['mailgun_domain']),
        'to': str(recipient),
        'subject': str(subject),
        'html': htmlMessage
    }

    resp, content = http.request(
        url, 'POST', urllib.urlencode(data),
        headers={"Content-Type": "application/x-www-form-urlencoded"})

    if resp.status != 200:
        raise RuntimeError(
            'Mailgun API error: {} {}'.format(resp.status, content))

def random_string(size=24, chars=string.ascii_letters + string.digits):
    """ Generate random string """

    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))
