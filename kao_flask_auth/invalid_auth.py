
class InvalidAuth(Exception):
    """ Represents an invalid Authentication Header """
    
    def __init__(self, code, description):
        """ Initialize with the code and exception """
        self.code = code
        self.description = description
        Exception.__init__(self, description)