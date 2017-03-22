#!/usr/bin/python
# coding: utf-8

from handlers.base import BaseHandler
from libs.decorators import logged_in
from models.user import User as UserModel
from libs import helper as Helper

class ListHandler(BaseHandler):

    @logged_in
    def get(self):
        output = []
        userQuery = UserModel.query()
        myUsers = userQuery.fetch()

        for user in myUsers:
            output.append(user.email)

        self.responseJSON('', **{
            'data': output
        })

class RegisterHandler(BaseHandler):

    def post(self):
        """ Process user register """

        message = []
        formData = self.parseBody(self.request.body)

        if self._validate(formData, message) == True:
            myUser = UserModel(
                email = str(formData['femail']),
                password = str(Helper.hash_password(formData['fpassword'])),
                groupid = 3
            )

            try:
                myUser.put()

                self.responseJSON('', **{
                    'msg': 'User register success.',
                    'data': {
                        'id': myUser.key.id()
                    }
                })
            except Exception as e:
                raise e
        else:
            self.responseJSON('DATA_VALIDATE_FAILED', **{'data': message})

    def _validate(self, formData, message):
        """ Validate request params """

        isOk = True

        if len(formData['fpassword']) == 0 or len(formData['fpassword']) < 8:
            isOk = False
            message.append('Password can not blank and > 8 character')

        if len(formData['frpassword']) == 0:
            isOk = False
            message.append('Repeat password can not blank')

        if formData['fpassword'] != formData['frpassword']:
            isOk = False
            message.append('Repeat password not match')

        if len(formData['femail']) == 0:
            isOk = False
            message.append('Email can not blank')

        if len(formData['femail']) > 0:
            userQuery = UserModel.query().filter(UserModel.email == formData['femail'])
            myUser = userQuery.fetch()

            if len(myUser) > 0:
                isOk = False
                message.append('Email already existed.')

        return isOk

class EmailLoginHandler(BaseHandler):

    def post(self):
        """ Login with email and password """

        message = []
        formData = self.parseBody(self.request.body)

        if self._validate(formData, message) == True:
            userQuery = UserModel.query().filter(UserModel.email == formData['femail']).filter(UserModel.password == Helper.hash_password(formData['fpassword']))
            myUser = userQuery.fetch()

            if len(myUser) > 0:
                payload = {
                    'id': myUser[0].key.id(),
                    'email': myUser[0].email,
                    'groupid': myUser[0].groupid,
                    'datecreated': Helper.datetimeToTimestamp(myUser[0].datecreated),
                }
                token = Helper.createToken(payload)

                self.responseJSON('', **{
                    'data': {
                        'token': token
                    }
                })
            else:
                self.responseJSON('DATA_NOTFOUND', **{
                    'data': [
                        'User not found.'
                    ]
                })
        else:
            self.responseJSON('DATA_VALIDATE_FAILED', **{'data': message})

    def _validate(self, formData, message):
        """ Validate request params """

        isOk = True

        if len(formData['fpassword']) == 0 or len(formData['fpassword']) < 8:
            isOk = False
            message.append('Password can not blank and > 8 character')

        if len(formData['femail']) == 0:
            isOk = False
            message.append('Email can not blank')

        return isOk
