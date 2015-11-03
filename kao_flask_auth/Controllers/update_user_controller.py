from ..token_builder import BuildToken

from flask import current_app as app
from kao_flask.ext.sqlalchemy import UpdateController, RecordValueProvider

def GetUpdateUserController(User, requires_auth):
    """ Return the UpdateUserController in the proper scope """
    class UpdateUserController(UpdateController):
        """ Controller to update a User """
        
        def __init__(self, toJson, recordValueProvider=None):
            """ Initialize the Update User Controller """
            self.toJson = toJson
            UpdateController.__init__(self, User, toJson, decorators=[requires_auth], 
                                      recordValueProvider=recordValueProvider)
        
        def performWithJSON(self, **kwargs):
            """ Remove the record """
            user = kwargs['user']
            updatedUser = UpdateController.update(self, user.id, kwargs['json'])
            return {"token": BuildToken(updatedUser, app.config['SECRET_KEY']), "user": self.toJson(updatedUser)}
    return UpdateUserController