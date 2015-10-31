from .invalid_auth import InvalidAuth
from .token_builder import VerifyToken, ExtractToken

from flask import current_app as app, request, jsonify
from flask.ext.httpauth import HTTPBasicAuth
from functools import wraps

def authenticate(error):
    resp = jsonify({'code':error.code, 'description':error.description})
    resp.status_code = 401
    return resp
    
class AuthRouteDecorator:
    """ Helper to provide a decorator to require authorization for a route """
    
    def __init__(self, UserCls):
        """ Initialize with the UserProxy Class to use """
        self.UserCls = UserCls
        
    def findUser(self):
        """ Find the User for the current request """
        auth = request.headers.get('Authorization', None)
        token = ExtractToken(auth)
        try:
            data = VerifyToken(token, app.config['SECRET_KEY'])
            user = self.UserCls.query.get(data['id'])
            return user
        except InvalidAuth as e:
            return authenticate(e)

    def requires_auth(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                user = self.findUser()
                kwargs['user'] = user
                return f(*args, **kwargs)
            except InvalidAuth as e:
                return authenticate(e)
        return decorated