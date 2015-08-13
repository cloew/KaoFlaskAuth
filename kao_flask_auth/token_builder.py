import jwt
    
def BuildToken(user, usernameField):
    """ Build the token """
    return str(jwt.encode({'id':user.id, usernameField:getattr(user, usernameField)}, 'secret token'))