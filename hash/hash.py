# ECE 544: Trustowrhty Computing - Final Project
# Creators: Nick DiMartino and Paul Joseph
# Topic: Internet of Things (IoT)
# Description of Code: Hashes passwords and creates command digest

import os
import hashlib
import base64


# Hash the passsord and add a salt
def hashed_pw(password,salt=None):
    # Example generation
    if salt == None:
        salt = os.urandom(32)

    key = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)

    # Store them as:

    storage = salt + key

    # Getting the values back o

    return storage
    

# Generates the session for the OS with a random password, salt, and key
def generate_session():
    pw = os.urandom(256)
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', pw, salt, 100000)

    return base64.b64encode(key).decode("utf-8")
