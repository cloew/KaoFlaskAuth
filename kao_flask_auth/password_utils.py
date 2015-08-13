import random
from hashlib import sha1

# borrowing these methods, slightly modified, from flask-peewee which in turn borrowed from django.contrib.auth
def get_hexdigest(salt, raw_password):
    data = salt + raw_password
    return sha1(data.encode('utf8')).hexdigest()

def make_password(raw_password):
    salt = get_hexdigest(random.random(), random.random())[:5]
    hsh = get_hexdigest(salt, raw_password)
    return '%s$%s' % (salt, hsh)

def check_password(raw_password, enc_password):
    salt, hsh = enc_password.split('$', 1)
    return hsh == get_hexdigest(salt, raw_password)