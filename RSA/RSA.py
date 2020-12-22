# ECE 544: Trustowrhty Computing - Final Project
# Creators: Nick DiMartino and Paul Joseph
# Topic: Internet of Things (IoT)
# Description of Code: RSA is a public-key cryptosystem that can generate a keypair as well as
# encrypt and decrpyt the key pairs given a plaintext and ciphertext while keeping them secret.

import rsa

# Generate the public key, private key keypair
def generate_keypair():
    (pub_key, priv_key) = rsa.key.newkeys(256)

    return (pub_key, priv_key)

# Encrpyt the private key and plaintext using RSA 
def encrypt(priv_key,plaintext):
    crypto = encrypt(plaintext, priv_key)

    return crypto

# Decrypt the public key and ciphertext using RSA
def decrypt(pub_key, ciphertext):
    crypto = decrypt(ciphertext, pub_key)

    return crypto