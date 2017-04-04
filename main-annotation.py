#!/usr/bin/env python
# *-* coding: UTF-8 *-*

import os
import sys
import json

# Third party libraries path must be fixed before importing webapp2
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'libs/external'))

import webapp2

from config import default as defaultConfig
from routes import annotation as annotationRoutes

webapp2Config = defaultConfig.config

app = webapp2.WSGIApplication(debug=os.environ['SERVER_SOFTWARE'].startswith('Dev'), config=webapp2Config)

# Routes add
annotationRoutes.add(app)
