from flask import app
from itsdangerous import JSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
import jwt
    
def BuildToken(user, usernameField):
    """ Build the token """
    s = Serializer(app.config['SECRET_KEY'])
    return s.dumps({ 'id': user.id })
        
def VerifyToken(token, UserCls):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        return None # invalid token
    return UserCls.query.get(data['id'])