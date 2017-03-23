#!/usr/bin/python
# coding: utf-8

from datetime import datetime
from handlers.base import BaseHandler
from libs.decorators import logged_in
from models.user import User as UserModel
from libs import helper as Helper

class ListHandler(BaseHandler):

    @logged_in
    def get(self, user):
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
            except:
                self.responseJSON('DATA_CREATE_FAILED')
                return

            self.responseJSON('', **{
                'message': 'User register success.',
                'data': {
                    'id': myUser.key.id()
                }
            })
        else:
            self.responseJSON('DATA_VALIDATE_FAILED', **{'data': message})
            return

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
                self.responseJSON('DATA_NOTFOUND')
                return
        else:
            self.responseJSON('DATA_VALIDATE_FAILED', **{'data': message})
            return

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

class ChangepasswordHandler(BaseHandler):

    @logged_in
    def post(self, user, id):
        message = []

        userId = int(id)
        formData = self.parseBody(self.request.body)

        if self._validate(formData, message) == True:
            if user['id'] != userId:
                self.responseJSON('TOKEN_NOT_MATCH_REQUEST')
                return

            myUser = UserModel.get_by_id(userId)

            if Helper.hash_password(formData['foldpassword']) != myUser.password:
                self.responseJSON('PASSWORD_NOT_MATCH')
                return

            # change password for user
            myUser.password = Helper.hash_password(formData['fnewpassword'])
            myUser.datechangepassword = datetime.now()

            try:
                myUser.put()
            except:
                self.responseJSON('DATA_UPDATE_FAILED')
                return

            self.responseJSON('', **{
                'message': 'User update success',
                'data': [
                    myUser.key.id()
                ]
            })

        else:
            self.responseJSON('DATA_VALIDATE_FAILED', **{'data': message})
            return

    def _validate(self, formData, message):
        """ Validate request params """

        isOk = True

        if len(formData['fnewpassword']) == 0 or len(formData['fnewpassword']) < 8:
            isOk = False
            message.append('New password can not blank and > 8 character')

        if len(formData['frpassword']) == 0 or len(formData['frpassword']) < 8:
            isOk = False
            message.append('Password repeat can not blank and > 8 character')

        if len(formData['foldpassword']) == 0 or len(formData['foldpassword']) < 8:
            isOk = False
            message.append('Old password can not blank and > 8 character')

        if formData['frpassword'] != formData['fnewpassword']:
            isOk = False
            message.append('Repeat password not match')

        return isOk
