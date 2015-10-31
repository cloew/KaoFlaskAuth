from functools import wraps
from flask import g
from flask.ext.httpauth import HTTPBasicAuth
from .token_builder import VerifyToken

auth = HTTPBasicAuth()

class AuthRouteDecorator:
    """ Helper to provide a decorator to require authorization for a route """
    
    def __init__(self, UserCls):
        """ Initialize with the UserProxy Class to use """
        self.UserCls = UserCls
        auth.verify_password(self.verify_password)
        
    def verify_password(self, token, password):
        """ Verify the User/password combination """
        user = VerifyToken(token, self.UserCls)
        if not user:
            return False
        g.user = user
        return True

    def requires_auth(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            kwargs['user'] = g.user
            return f(*args, **kwargs)
        return auth.login_required(decorated)