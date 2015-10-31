from passlib.apps import custom_app_context

def make_password(raw_password):
    return pwd_context.encrypt(raw_password)

def check_password(raw_password, enc_password):
    return pwd_context.verify(raw_password, enc_password)