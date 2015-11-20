from ..errors import Errors
from ..password_util import PasswordUtil

from kao_flask.ext.sqlalchemy import CreateController
from sqlalchemy.exc import IntegrityError

def GetRegisterController(User, LoginController):
    """ Return the RegisterController in the proper scope """
    class RegisterController(CreateController):
        """ Controller to register a user """
        
        def __init__(self, toJson, passwordUtil=None, recordValueProvider=None):
            """ Initialize the Register Controller """
            self.passwordUtil = PasswordUtil() if passwordUtil is None else passwordUtil
            self.loginController = LoginController(toJson, passwordUtil=passwordUtil)
            CreateController.__init__(self, User, None, recordValueProvider=recordValueProvider)
        
        def performWithJSON(self, json=None):
            """ Create a User record with the given credentials """
            try:
                createKwargs = dict(json)
                createKwargs['password'] = self.passwordUtil.make(json['password'])
                user = self.create(createKwargs)
                return self.loginController.performWithJSON(json=json)
            except IntegrityError:
                return Errors.EMAIL_IN_USE.toJSON()
    return RegisterController