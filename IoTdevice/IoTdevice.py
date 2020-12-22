# ECE 544: Trustowrhty Computing - Final Project
# Creators: Nick DiMartino and Paul Joseph
# Topic: Internet of Things (IoT)
# Description of Code: Simulated IoT device used in the secure architecture communcation.  This 
# verifies the signature and executes the commands given.

import os
import socket
import rsa
import hash
import base64
import dotenv

dotenv.load_dotenv()     # reads and loads the key-value pair

# Host, Port, and Deivce names for the communcation
HOST = 'localhost'
PORT = 8082
DEVICE = "Roku Smart TV"

# Generated private key and hash for the secure communcation
priv=rsa.PrivateKey(3247, 65537, 833, 191, 17)
priv = priv.load_pkcs1(base64.b64decode(os.getenv("PRIVATE_KEY")))
hashsalt = base64.b64decode(os.getenv("HASH_SALT"))


# Signs the message with the hash
def sign(message):
    digest = hash.hashed_pw(message, hashsalt)

    return digest


# Validates the digital signature for a secure communcation with the client and IoT device
def validate_digitalsignature(digest):
    command_digest = sign(digest[0])                                                # signs the command
    halfsig = rsa.decrypt(base64.b64decode(digest[1]), priv)                        # decrypt the first half of the signature
    halfsig2 = rsa.decrypt(base64.b64decode(digest[2]), priv)                       # decrypt the second half of the signature
    print('command digest:',command_digest[33:54],command_digest[54:64])
    print('Decrypted signature:', halfsig, halfsig2)

    # If the command matches the decrypted signature, the the digital signature is verified
    if command_digest[33:54] == halfsig and command_digest[54:64] == halfsig2:      
        return True

    return False


# Execute the given command from the client
def execute_command(response):
    digest = response.decode().split('|')

    if validate_digitalsignature(digest) == True:
        execution = digest[0] + " EXECUTED!|-{}".format(DEVICE)
        return execution.encode()
    else:
        return b"Invalid signature!"


# Create the network communicatioon over the HOST and PORT for to connect with the IoT server and Client
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))

    while True:
        bytesAddressPair = s.recvfrom(1024)
        data = bytesAddressPair[0]

        address = bytesAddressPair[1]

        response = execute_command(data)
        print("Response sent")
        s.sendto(response, address)
