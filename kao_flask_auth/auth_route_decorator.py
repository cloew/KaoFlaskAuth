from functools import wraps
from flask import request, jsonify
import jwt

class AuthRouteDecorator:
    """ Helper to provide a decorator to require authorization for a route """
    
    def __init__(self, UserProxyCls):
        """ Initialize with the UserProxy Class to use """
        self.UserProxyCls = UserProxyCls
        
    def failAuthentication(self, error):
        """ Return the proper error Json and error code """
        resp = jsonify(error)
        resp.status_code = 401
        return resp
        
    def extractToken(self):
        """ Return the token and/or error """
        auth = request.headers.get('Authorization', None)
        if not auth:
          return None, {'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}

        parts = auth.split()

        if parts[0].lower() != 'bearer':
          return None, {'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}
        elif len(parts) == 1:
          return None, {'code': 'invalid_header', 'description': 'Token not found'}
        elif len(parts) > 2:
          return None, {'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}

        return parts[1], None

    def requires_auth(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token, error = self.extractToken()
            if error is not None:
                return self.failAuthentication(error)
                
            try:
                payload = jwt.decode(token.encode('utf-8'), 'secret token')
                # payload = jwt.decode(
                    # token,
                    # base64.b64decode(env["AUTH0_CLIENT_SECRET"].replace("_","/").replace("-","+"))
                # )
            # except jwt.ExpiredSignature:
                # return authenticate({'code': 'token_expired', 'description': 'token is expired'})
            except jwt.DecodeError as e:
                print(e)
                return self.failAuthentication({'code': 'token_invalid_signature', 'description': 'token signature is invalid'})

            # if payload['aud'] != env["AUTH0_CLIENT_ID"]:
              # return authenticate({'code': 'invalid_audience', 'description': 'the audience does not match. expected: ' + CLIENT_ID})
              
            kwargs['user'] = self.UserProxyCls(payload).user
            return f(*args, **kwargs)
        return decorated