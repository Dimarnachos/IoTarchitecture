# ECE 544: Trustowrhty Computing - Final Project
# Creators: Nick DiMartino and Paul Joseph
# Topic: Internet of Things (IoT)
# Description of Code: The user will send his or her username and server ID here, the Authentication Server (AS).
# The AS will then find the key in the database that corresponds to the given username and password.  If found, the
# AS responds to user with a generated ticket, with a finite lifetime, and a session  key.  These are then sealed
# with the server key and then the entire message is sealed with the clients key.  

import os
import socket
from datetime import datetime, timedelta
import hash
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import DES
import base64
import dotenv

dotenv.load_dotenv()   # reads and loads the key-value pair 

# Host and port for server and client communcation
HOST = '127.0.0.1'
PORT = 8081

# Key for the IoT server/device
IOTKEY = base64.b64decode(os.getenv("IOTKEY"))

# Database config for user
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
i = 0

# Class for the user and his or her username, server, and password
class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String, primary_key=True)    # puts the user's username in a column
    server = db.Column(db.String, primary_key=True)      # puts the user's server in a column
    password = db.Column(db.String)                      # puts the user's password in a column
    __table_args__ = {'schema': 'Users'}                 # labels the columns


# Generates the session with the given username and password
def generate_session(username, password, servername, network_address):
    global i
    i+=1
    key = hash.generate_session()                                  # key for the session
    dateTimeObj = datetime.now()                                   # gets the current timestamp
    timestampStr = dateTimeObj.strftime("%Y-%m-%d %H:%M:%S.%f")    # converts the timestamp to a readable format
    life = str(dateTimeObj + timedelta(hours=1))                   # lifetime for the generated ticket

    print(i, timestampStr)


    # Create the ticket with correct parameters and encrypt it using DES
    ticket = '{{"username":"{}","server":"{}","network":"{}","sessionkey":"{}","timestamp":"{}","lifetime":"{}"}}'.format(
        username, servername, network_address, key, timestampStr, life)
    print(i,ticket)
    eTicket = DES.encrypt(IOTKEY[:8], ticket)
    eticket_str = base64.b64encode(eTicket).decode("utf-8")
    payload = '{{"sessionkey":"{}","timestamp":"{}","lifetime":"{}","ticket":"{}"}}'.format(key, timestampStr, life,
                                                                                            eticket_str)

    # # Encrypt the client's key using DES
    client_key = base64.b64decode(password)
    cipher = DES.encrypt(client_key[48:56], payload)

    # Add a salt to the password hash and return the packet
    salt = base64.b64encode(client_key[:32]).decode("utf-8")
    return_packet = '{{"salt":"{}","payload":"{}"}}'.format(salt, base64.b64encode(cipher).decode("utf-8"))
    return return_packet.encode()


# Create the network communicatioon over the HOST and PORT for to connect with the Client and Database
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))         # assigns IP address and port number to socket instance
    s.listen()                   # make the sockety ready for communcation
    conn, addr = s.accept()      # accept the incoming connection request
    with conn:
        print('Connected by', addr)

        while True:
            data = conn.recv(1024)                                                                 # receives data from both TCP and UDP
            parts = data.decode().split('|')                                                       # converts the string to a number
            user = User.query.filter_by(username=parts[0], server=parts[1]).first()                # filter the decoded message
            if user:
                packet = generate_session(user.username, user.password, user.server, str(addr))    # get the packet from the session
                conn.sendall(packet)                                                               # sends the packet
            else:
                conn.sendall("Nice try buddie ;-)".encode())                                       # doesn't send the packet
