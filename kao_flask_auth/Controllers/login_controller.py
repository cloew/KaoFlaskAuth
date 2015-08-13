from ..errors import Errors
from ..password_utils import check_password
from ..token_builder import BuildToken

from kao_flask import JSONController

def GetLoginController(User):
    """ Return the LoginController in the proper scope """
    class LoginController(JSONController):
        """ Controller to login a user """
        
        def __init__(self, toJson):
            """ Initialize with the mthod to convert to JSON """
            self.toJson = toJson
            JSONController.__init__(self)
        
        def performWithJSON(self, json=None):
            """ Create a User record with the given credentials """
            user = User.query.filter_by(email=json['email']).first()
            if user and check_password(json['password'], user.password):
                return {'token':BuildToken(user), 'user':self.toJson(user)}, 201
            else:
                return Errors.INVALID_CREDS.toJSON()
    return LoginController