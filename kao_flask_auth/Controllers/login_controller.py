from ..errors import Errors
from ..password_util import PasswordUtil
from ..token_builder import BuildToken

from flask import current_app as app
from kao_flask import JSONController
from kao_flask.ext.sqlalchemy import db

def GetLoginController(User, usernameField):
    """ Return the LoginController in the proper scope """
    class LoginController(JSONController):
        """ Controller to login a user """
        
        def __init__(self, toJson, passwordUtil=None, legacyUtils=[]):
            """ Initialize with the mthod to convert to JSON """
            self.toJson = toJson
            self.passwordUtil = PasswordUtil() if passwordUtil is None else passwordUtil
            self.legacyUtils = legacyUtils
            JSONController.__init__(self)
        
        def performWithJSON(self, json=None):
            """ Create a User record with the given credentials """
            filterKwargs = {usernameField: json[usernameField]}
            user = User.query.filter_by(**filterKwargs).first()
            if user and self.validPassword(user, json['password']):
                return {'token':BuildToken(user, app.config['SECRET_KEY']), 'user':self.toJson(user)}, 201
            else:
                return Errors.INVALID_CREDS.toJSON()
                
        def validPassword(self, user, password):
            """ Return if the user's password is valid """
            try:
                if self.passwordUtil.check(password, user.password):
                    return True
            except ValueError:
                pass
                
            for util in self.legacyUtils:
                if util.check(password, user.password):
                    user.password = self.passwordUtil.make(password)
                    db.session.add(user)
                    db.session.commit()
                    return True
            else:
                return False
            
    return LoginController