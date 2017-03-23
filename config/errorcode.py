#!/usr/bin/python
# coding: utf-8

error = {
    'DATA_VALIDATE_FAILED': {
        'error_code': 1001,
        'dev_message': 'Form data validation failed',
        'status_code': 400
    },
    'DATA_CREATE_FAILED': {
        'error_code': 1002,
        'dev_message': 'Entity can not put to datastore',
        'status_code': 400
    },
    'DATA_NOTFOUND': {
        'error_code': 1003,
        'dev_message': 'Request resource not found in server',
        'status_code': 404
    },
    'DATA_UPDATE_FAILED': {
        'error_code': 1004,
        'dev_message': 'Entity can not put to datastore via update method',
        'status_code': 400
    },
    'TOKEN_EXPIRED': {
        'error_code': 2001,
        'dev_message': 'JWT token date expired',
        'status_code': 400
    },
    'TOKEN_NOT_MATCH_REQUEST': {
        'error_code': 2002,
        'dev_message': 'JWT token not match with user id request',
        'status_code': 400
    },
    'TOKEN_INVALID_TIME': {
        'error_code': 2003,
        'dev_message': 'JWT token just changed by user, may be user change password',
        'status_code': 400
    },
    'PASSWORD_NOT_MATCH': {
        'error_code': 3000,
        'dev_message': 'Password user request not match with current password of user',
        'status_code': 400
    }
}
