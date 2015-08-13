from .auth_route_decorator import AuthRouteDecorator
from .user_proxy import GetUserProxy
from .Controllers import GetAuthJsonController, GetCurrentUserController, GetLoginController, GetRegisterController, GetUpdateUserController

from kao_decorators import proxy_for, lazy_property

@proxy_for('authRouteDecorator', ['requires_auth'])
class KaoAuth:
    """ Helper class to use to generate the Auth funcitonality based on a provided User class """
    
    def __init__(self, userCls):
        """ Initialize with the User Class to use """
        self.userCls = userCls
        self.userProxyCls = GetUserProxy(userCls)
        self.authRouteDecorator = AuthRouteDecorator(self.userProxyCls)
        
    @lazy_property
    def JSONController(self):
        """ Return the Auth JSON Controller class for the User model """
        return GetAuthJsonController(self.requires_auth)
        
    @lazy_property
    def CurrentUserController(self):
        """ Return the Current User Controller class for the User model """
        return GetCurrentUserController(self.JSONController)
        
    @lazy_property
    def LoginController(self):
        """ Return the Login Controller class for the User model """
        return GetLoginController(self.userCls)
        
    @lazy_property
    def RegisterController(self):
        """ Return the Register Controller class for the User model """
        return GetRegisterController(self.userCls, self.LoginController)
        
    @lazy_property
    def UpdateUserController(self):
        """ Return the Update User Controller class for the User model """
        return GetUpdateUserController(self.userCls, self.requires_auth)