from ..errors import Errors
from ..password_utils import make_password

from kao_flask.ext.sqlalchemy import CreateController
from sqlalchemy.exc import IntegrityError

def GetRegisterController(User, LoginController):
    """ Return the RegisterController in the proper scope """
    class RegisterController(CreateController):
        """ Controller to register a user """
        
        def __init__(self, recordValueProvider=None):
            """ Initialize the Register Controller """
            CreateController.__init__(self, User, None, recordValueProvider=recordValueProvider)
        
        def performWithJSON(self, json=None):
            """ Create a User record with the given credentials """
            try:
                json['password'] = make_password(json['password'])
                user = self.create(json)

                login = LoginController()
                return login.performWithJSON(json=json)
            except IntegrityError:
                return Errors.EMAIL_IN_USE.toJSON()
    return RegisterController