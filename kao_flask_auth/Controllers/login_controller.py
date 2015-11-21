from ..errors import Errors
from ..password_scheme import PasswordScheme
from ..token_builder import BuildToken

from flask import current_app as app
from kao_flask import JSONController
from kao_flask.ext.sqlalchemy import db

def GetLoginController(User, usernameField):
    """ Return the LoginController in the proper scope """
    class LoginController(JSONController):
        """ Controller to login a user """
        
        def __init__(self, toJson, pwdScheme=None, legacySchemes=[]):
            """ Initialize with the mthod to convert to JSON """
            self.toJson = toJson
            self.pwdScheme = PasswordScheme() if pwdScheme is None else pwdScheme
            self.legacySchemes = legacySchemes
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
                if self.pwdScheme.check(password, user.password):
                    return True
            except ValueError:
                pass
                
            for scheme in self.legacySchemes:
                if scheme.check(password, user.password):
                    user.password = self.pwdScheme.make(password)
                    db.session.add(user)
                    db.session.commit()
                    return True
            else:
                return False
            
    return LoginController