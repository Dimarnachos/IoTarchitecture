ECE 544: Trustowrthy Computing
Nick DiMartino and Paul Joseph
Internet of Things
Project Overview

IoT Architecture - How it Works
1. User signs onto client and requests access to server by sending username and server ID to AS.
           client.py --> AuthenticatioServer.py
2. AS finds the corresponding key in the database.
           AuthenticationServer.py <--> database
3. AS responds with generated ticket with a finite lifetime and sessions key, seals the ticket with server key, and then seals entire message with clients key.
           AuthenticationServer.py --> client.py
4. User decrypts message with it's key (password) and retrieves session key. Authenticator is generates and the session key is used to seal it.  The signed requests, session ticket, and authenticator are sent to the IoT server.
           client.py --> IoTserver.py
5. The IoT server decrypts the session ticket with its key, retrieves the session key, and verifies session. Signed request is then forwarded to the IoT device.
           IoTserver.py --> IoTdevice.py
6. The IoT device decrypts the signature with the public key and matches it with the hashed message, validates it, and then executes the request.
           IoTdevice.py --> IoTserver.py
7. The server then responds with confirmation of the executed request.
           IoTserver.py --> client.py

Possible Improvements

Some possible improvements can be made to the user authentication process where if you enter the wrong password the delay to prompt you to retry is longer than if you entered the wrong username which adversaries can possibly interpret the method in which users are being authenticated. This delay is cause due to the AS returning the session ticket and the client trying to decrypt it with the wrong password, to improve this a time delay can be added to the client side when a user enters the wrong password so the adversary would not be able to make a difference. In addition to that, we can add a limit on wrong username/password attempts to prevent any brute force attempts. 

Tests

We tested are implementation by entering wrong passwords/usernames which never resulted in a wrongful authentication. We also altered the clients public key, which would result in an Invalid signature error. We also tried to reuse the same client request to the IoTServer, which would result in an invalid session.  

Setup
To run this project you will need to install the following libraries, WE will also include the commands needed to install them in bash:
Flask -  pip install Flask
Flask-sqlalchemy - pip install flask-sqlalchemy
Python-dotenv - pip install python-dotenv
Python-DES -  pip install des 
Python-RSA - pip install rsa

Once these libraries are installed, you will need to setup a database(We used a PostgreSQL database) to work as the key distribution center that the AS will connect to. Once the database is set up you must add the database URI into the .env file located in the root of the zip file, it may be hidden so you can unhide it in macOS using this command "Command+Shift+Dot". The .env file includes private information such as the clients public key, and IoTdevice private key. In addition, it includes the IoT key shared between the AS and the IoTServer. Moving on, once the DB is setup you will have to add a USER entity to the database. You can do this by doing the following in your python interpreter:

1. "from AuthenticationServer import db, User"
2. "import hash"
3. "import base64"
4. pw= hash.hashed_pw("yourpassword")
5. pw = base64.b64encode(pw).decode("utf-8")
2. user = User(username="yourusername",password=pw,server="IoTServer") 
3. db.session.add(user)
4. db.session.commit()

Once the database is all setup you are good to go. To run the program you must run all of the servers before running the client in separate terminal processes. E.g. to run the IoTdevice server, run the command "python IoTdevice.py" in a terminal window. 

Once all the servers are running you can now run the client in a separate window, enter your username and password. You will now be logged in and able to interact with the IoTdevice.


