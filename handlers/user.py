#!/usr/bin/python
# coding: utf-8

from datetime import datetime, timedelta
from handlers.base import BaseHandler
from libs.decorators import logged_in
from models.user import User as UserModel
from libs import helper as Helper
from google.appengine.api import mail
from config import default as defaultConfig

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
            codeActivation = Helper.random_string()

            myUser = UserModel(
                email = str(formData['femail']),
                password = str(Helper.hash_password(formData['fpassword'])),
                groupid = 3,
                status = UserModel.STATUS_INACTIVE,
                code_activation = codeActivation
            )

            try:
                myUser.put()
            except:
                self.responseJSON('DATA_CREATE_FAILED')
                return

            # send email activation
            mailTemplate = 'mail_templates/account_activate.html'
            with open(mailTemplate) as f:
                htmlBody = f.read()

            userActivationLink = self.getHostname() + '/api/user/activation?e='+ myUser.email +'&c=' + codeActivation
            messageBody = htmlBody.format(activation_url=userActivationLink)

            Helper.send_mail(messageBody, 'Welcome to Olli-AI', myUser.email)

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
            myUsers = userQuery.fetch()

            if len(myUsers) > 0:
                # denied if user not active
                if myUsers[0].status == UserModel.STATUS_INACTIVE:
                    self.responseJSON('USER_INACTIVE')
                    return

                payload = {
                    'id': myUsers[0].key.id(),
                    'email': myUsers[0].email,
                    'groupid': myUsers[0].groupid,
                    'status': myUsers[0].status,
                    'date_created': Helper.datetimeToTimestamp(myUsers[0].date_created),
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
    def post(self, user, userId):
        message = []

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
            myUser.date_change_password = datetime.now()

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

class LogoutHandler(BaseHandler):

    @logged_in
    def post(self, user):
        message = []

        userQuery = UserModel.query().filter(UserModel.email == user['email']).filter(UserModel.status == UserModel.STATUS_ACTIVE)
        myUsers = userQuery.fetch()

        if len(myUsers) > 0:
            if myUsers[0].status == UserModel.STATUS_INACTIVE:
                self.responseJSON('USER_INACTIVE')
                return
            else:
                # update user status to STATUS_LOGOUT
                myUsers[0].status = UserModel.STATUS_LOGOUT

                try:
                    myUsers[0].put()
                except:
                    self.responseJSON('DATA_UPDATE_FAILED')
                    return

                self.responseJSON('', **{
                    'message': 'User logout success',
                    'data': []
                })
        else:
            self.responseJSON('DATA_NOT_FOUND')
            return

class ActivationHandler(BaseHandler):

    def get(self):
        message = []

        userEmail = self.request.get('e')
        userCode = self.request.get('c')

        userQuery = UserModel.query().filter(UserModel.email == userEmail).filter(UserModel.code_activation == userCode)
        myUsers = userQuery.fetch()

        if len(myUsers) > 0:
            # compare date_created expire time
            expiredTime = myUsers[0].date_created + timedelta(seconds=defaultConfig.config['account_activation_expire'])

            if expiredTime < datetime.utcnow():
                self.responseJSON('USER_ACTIVATION_EXPIRE')
                return
            else:
                # update user status to ACTIVE
                myUsers[0].status = UserModel.STATUS_ACTIVE

                try:
                    myUsers[0].put()
                except:
                    self.responseJSON('DATA_UPDATE_FAILED')
                    return

                self.responseJSON('', **{
                    'message': 'Account activated success',
                    'data': [
                        myUsers[0].key.id()
                    ]
                })
        else:
            self.responseJSON('DATA_NOTFOUND')
            return
