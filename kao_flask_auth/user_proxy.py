from kao_decorators import lazy_property

def GetUserProxy(UserCls):
    """ Return the User Proxy Class for the given User Cls """
    class UserProxy:
        """ Represents a proxy to lazy load a User object """
        
        def __init__(self, userInfo):
            """ Initialize the proxy with the user info """
            self.userInfo = userInfo
            
        @lazy_property
        def user(self):
            """ Lazy load the user """
            return UserCls.query.filter_by(id=self.userInfo[u'id']).first()
            
        def exists(self):
            """ Return if the User record actually exists """
            return self.user is not None
        
        def __nonzero__(self):
            """ Return if the object is true """
            return self.exists()
    return UserProxy