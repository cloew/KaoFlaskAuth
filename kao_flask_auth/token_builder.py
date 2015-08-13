import jwt
    
def BuildToken(user):
    """ Build the token """
    return jwt.encode({'id':user.id, 'email':user.email}, 'secret token')