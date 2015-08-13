from enum import Enum

class Errors(Enum):
    """ Represents a Server Error """
    INVALID_CREDS = 1, 'Invalid Credentials'
    EMAIL_IN_USE = 2, 'The provided email address is already in use'
    NO_USER = 3, 'The requested user could not be found'

    
    def __init__(self, code, message):
        """ Initialize the Error with its code and message """
        self.code = code
        self.message = message
        
    def toJSON(self):
        """ Transform the error into JSON """
        return {'error':{'code':self.code, 'message':self.message}}
        