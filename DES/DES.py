# ECE 544: Trustowrhty Computing - Final Project
# Creators: Nick DiMartino and Paul Joseph
# Topic: Internet of Things (IoT)
# Description of Code: This is the symmetric-key algorithm called Data Encryption Standard (DES).
# This code generates a key as well as encrypt and decrypt given keys

from des import DesKey


# Generate a key using DES
def generate_key(key):
    key = DesKey(key)
    return key


# Encrpyt a key and plaintext using DES 
def encrypt(key, plaintext):

    key0 = generate_key(key)

    ciphertext = key0.encrypt(plaintext.encode(),padding=True)
    return ciphertext


# Decrypt a key and ciphertext using DES
def decrypt(key, ciphertext):
    key0 = generate_key(key)
    plaintext = key0.decrypt(ciphertext, padding=True)
    return plaintext
