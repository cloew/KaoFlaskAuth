import jwt
    
def BuildToken(user, usernameField):
    """ Build the token """
    token = jwt.encode({'id':user.id, usernameField:getattr(user, usernameField)}, 'secret token')
    return token.decode('utf-8')