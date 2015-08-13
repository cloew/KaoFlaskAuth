from kao_flask import JSONController

def GetAuthJsonController(requires_auth):
    """ Return the AuthJsonController in the proper scope """
    
    class AuthJSONController(JSONController):
        """ Controller Base that requires the user to be authorized before running """
        
        def __init__(self):
            """ Initialize the JSON Controller with its required decorators """
            JSONController.__init__(self, decorators=[requires_auth])
    return AuthJSONController