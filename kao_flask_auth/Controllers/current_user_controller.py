from ..errors import Errors

def GetCurrentUserController(AuthJSONController):
    """ Return the CurrentUserController in the proper scope """
    class CurrentUserController(AuthJSONController):
        """ Controller to return the currently signed in user """
        
        def __init__(self, toJson):
            """ Initialize with the Json Converter """
            self.toJson = toJson
            AuthJSONController.__init__(self)
        
        def performWithJSON(self, json=None, user=None):
            """ Convert the existing Word Lists to JSON """
            if user:
                return {'user':toJson(user)}
            return Errors.NO_USER.toJSON()
    return CurrentUserController