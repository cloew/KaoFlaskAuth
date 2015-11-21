from passlib.apps import custom_app_context
    
class PasswordScheme:
    """ Helper class to make and check passwords """
    
    def make(self, raw_password):
        """ Return the hashed password """
        return custom_app_context.encrypt(raw_password)
        
    def check(self, raw_password, enc_password):
        """ Return if the Passowrd provided is valid """
        return custom_app_context.verify(raw_password, enc_password)