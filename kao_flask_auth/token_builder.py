from .invalid_auth import InvalidAuth
from itsdangerous import JSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
    
def BuildToken(user, secret):
    """ Build the token """
    s = Serializer(secret)
    return s.dumps({ 'id': user.id }).decode('utf-8')
        
def VerifyToken(token, secret):
    s = Serializer(secret)
    try:
        data = s.loads(token)
    except BadSignature as e:
        raise InvalidAuth('bad_token', e.message)
    return data
    
def ExtractToken(auth):
    """ Extract the Authentication Token from the Request Header """
    if not auth:
        raise InvalidAuth('authorization_header_missing', 'Authorization header is expected')

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        raise InvalidAuth('invalid_header', 'Authorization header must start with Bearer')
    elif len(parts) == 1:
        raise InvalidAuth('invalid_header', 'Token not found')
    elif len(parts) > 2:
        raise InvalidAuth('invalid_header', 'Authorization header must be Bearer + \s + token')
    return parts[1]