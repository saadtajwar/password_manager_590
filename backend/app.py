import os
import psycopg2
import bcrypt
from base64 import b64encode, b64decode
from dotenv import load_dotenv
from flask import Flask, request, session
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESSIV
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from Crypto.PublicKey import RSA
from Crypto.Hash import HMAC
from struct import pack

load_dotenv()

app = Flask(__name__)
app.secret_key = "secret"
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

# Database: PasswordManager 
# Table 1: Users
#   -> userId (unique)
#   -> name
#   -> email(unique)
#   -> password
# Table 2: <passwords-user_id>
#   -> website (unique)
#   -> alias
#   -> password
#   -> shared_with_me: boolean
#   -> shared_with_others boolean
#   -> shared_list

CREATE_USERS_TABLE = (
    "CREATE TABLE IF NOT EXISTS users (user_id SERIAL PRIMARY KEY, name VARCHAR(100) NOT NULL, email VARCHAR(100) NOT NULL UNIQUE, password TEXT NOT NULL, public_key TEXT NOT NULL, key_salt TEXT NOT NULL);"
)

CREATE_PASSWORDS_TABLE = (
    "CREATE TABLE IF NOT EXISTS passwords%s (website TEXT, alias TEXT, password TEXT, is_owner BOOLEAN, shared_list INTEGER[]);"
)

GET_USER_PASSWORD = (
    "SELECT password FROM users WHERE email=%s;"
)

GET_USER_ID = (
    "SELECT user_id FROM users WHERE email=%s;"
)

GET_PASSWORDS = (
    "SELECT website, alias, password, is_owner, shared_list FROM passwords%s;"
)

GET_PASSWORD_AND_ALIAS_FOR_WEBSITE = (
    "SELECT alias, password FROM passwords%s WHERE website = %s"
)

GET_KEY_SALT = (
    "SELECT key_salt FROM users WHERE email = %s"
)

INSERT_USER_RETURN_ID = (
    "INSERT INTO users (name, email, password, public_key, key_salt) VALUES (%s, %s, %s, %s, %s) RETURNING user_id;"
)

INSERT_PASSWORDS = (
    "INSERT INTO passwords%s (website, alias, password, is_owner, shared_list) VALUES (%s, %s, %s, %s, %s)"
)

DELETE_USER_PASSWORDS = (
    "DROP TABLE passwords%s;"
)

DELETE_USER = (
    "DELETE FROM users WHERE user_id = %s"
)

DELETE_PASSWORD = (
    "DELETE FROM passwords%s WHERE website = %s"
)
    
UPDATE_PASSWORD = (
    "UPDATE passwords%s SET password = %s WHERE website = %s;"
)
    
ADD_TO_SHARED_LIST = (
    "UPDATE passwords%s SET shared_list = (SELECT shared_list FROM passwords%s WHERE website = %s) || ARRAY[%s] WHERE website = %s;"
)

REMOVE_FROM_SHARED_LIST = (
    "UPDATE passwords%s SET shared_list = (ARRAY_REMOVE((SELECT shared_list FROM passwords%s WHERE website = %s), %s)) WHERE website = %s"
)

# Registers a user - adds new user to users table and creates their password table
@app.post("/api/users")
def add_user():
    data = request.get_json()
    name, email, password = data["name"], data["email"], data["password"]
    with connection:
        with connection.cursor() as cursor:
            # Create Users table if it doesn't already exist
            cursor.execute(CREATE_USERS_TABLE)
            # Hash master password before storing
            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
            # Generate the user's master key
            key_salt = os.urandom(16)
            kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=64, salt=key_salt, iterations=100000)
            master_key = kdf.derive(password.encode('utf-8'))
            # Generate RSA key pair in pycryptodome
            pycrypto_private_key = RSA.generate(2048, PRNG(master_key))
            pycrypto_public_key = pycrypto_private_key.publickey()
            # Encode keys in PEM format
            private_key_pem = pycrypto_private_key.export_key()
            public_key_pem = pycrypto_public_key.export_key()
            # Enter new user into Users table
            cursor.execute(INSERT_USER_RETURN_ID, (name, email, password_hash, public_key_pem.decode('ascii'), b64encode(key_salt).decode('utf-8')))
            user_id = cursor.fetchone()[0]
            # Store the user ID, master key, and private key in session variables to avoid recomputation cost
            session["user_id"] = user_id
            session["master_key"] = b64encode(master_key).decode('utf-8')
            session["private_key"] = private_key_pem.decode('ascii')
            # Create the user's Passwords table
            cursor.execute(CREATE_PASSWORDS_TABLE, (user_id, ))
    return {"id": user_id, "message": f"User {user_id} added."}, 201

# Deletes a user from the users table and deletes their passwords table
@app.delete("/api/users/<int:user_id>")
def delete_user(user_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_USER_PASSWORDS, (user_id, ))
            cursor.execute(DELETE_USER, (user_id, ))
    return {"message": f"User {user_id} deleted."}, 200

# Authenticates a user when provided with email and password - returns user's user_id if valid
@app.get("/api/users/login")
def authenticate():
    data = request.get_json()
    email, password = data["email"], data["password"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_USER_PASSWORD, (email, ))
            user_info = cursor.fetchone()
            if user_info is not None:
                password_hash = user_info[0].encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), password_hash):
                    # Get user ID
                    cursor.execute(GET_USER_ID, (email, ))
                    user_id = cursor.fetchone()[0]
                    # Get the user's key salt
                    cursor.execute(GET_KEY_SALT, (email, ))
                    key_salt = b64decode(cursor.fetchone()[0].encode('utf-8'))
                    # Calculate user's master key
                    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=64, salt=key_salt, iterations=100000)
                    master_key = kdf.derive(password.encode('utf-8'))
                    # Calculate user's private RSA key and encode it in PEM format
                    pycrypto_private_key = RSA.generate(2048, PRNG(master_key))
                    private_key_pem = pycrypto_private_key.export_key()
                    # Store the user ID, master key, and private key in session variables to avoid recomputation cost
                    session["user_id"] = user_id
                    session["master_key"] = b64encode(master_key).decode('utf-8')
                    session["private_key"] = private_key_pem.decode('ascii')
                    return {"message": "Authentication successful", "user_id": user_id}, 200
    return {"message": "Authentication failed"}, 401

# Fetches list of user's passwords in (website, alias, password) form
@app.get("/api/users/<int:user_id>")
def get_user(user_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_PASSWORDS, (user_id, ))
            passwords = cursor.fetchall()
    return {"passwords": passwords, "message": "Passwords fetched successfully"}, 200

# Adds a credential to the user's password table
@app.post("/api/users/<int:user_id>/add")
def add_credential(user_id):
    data = request.get_json()
    website, alias, password =  data["website"], data["alias"], data["password"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_PASSWORDS, (user_id, website, alias, password, True, f"{{}}", ))
    return {"message": f"Password for {website} inserted"}, 200

# Updates a credential in the user's password table
@app.post("/api/users/<int:user_id>/update")
def update_credential(user_id):
    data = request.get_json()
    website, password = data["website"], data["password"]
    with connection:
        with connection.cursor() as cursor:
            # TODO: only allow update if user is owner of password
            cursor.execute(UPDATE_PASSWORD, (user_id, password, website))
            # TODO: update password in shared users' tables
    return {"message": f"Password for {website} updated"}, 200

# Deletes a credential in the user's password table
@app.post("/api/users/<int:user_id>/delete")
def delete_credential(user_id):
    data = request.get_json()
    website = data["website"]
    with connection:
        with connection.cursor() as cursor:
            # TODO: only allow deletion if user is owner of password
            cursor.execute(DELETE_PASSWORD, (user_id, website))
            # TODO: delete password from shared users tables
    return {"message": f"Password for {website} deleted"}, 200

# Shares a user's credential with another user given the website and user email
@app.post("/api/users/<int:user_id>/share")
def share_credential(user_id):
    data = request.get_json()
    website, email = data["website"], data["email"]
    with connection:
        with connection.cursor() as cursor:
            # TODO: only allow share if user is owner of password
            cursor.execute(GET_USER_ID, (email, ))
            other_user_id = cursor.fetchone()[0]
            cursor.execute(ADD_TO_SHARED_LIST, (user_id, user_id, website, other_user_id, website))
            cursor.execute(GET_PASSWORD_AND_ALIAS_FOR_WEBSITE, (user_id, website))
            alias_and_password = cursor.fetchone()
            alias, password = alias_and_password[0], alias_and_password[1]
            cursor.execute(INSERT_PASSWORDS, (other_user_id, website, alias, password, False, f"{{ {user_id} }}"))
    return {"message": "Password shared successfully"}, 200


# Unshares a user's credential with a given user
@app.post("/api/users/<int:user_id>/unshare")
def unshared_credential(user_id):
    data = request.get_json()
    website, email = data["website"], data["email"]
    with connection:
        with connection.cursor() as cursor:
            # TODO: only allow unshare if user is owner of password
            cursor.execute(GET_USER_ID, (email, ))
            other_user_id = cursor.fetchone()[0]
            cursor.execute(REMOVE_FROM_SHARED_LIST, (user_id, user_id, website, other_user_id, website))
            cursor.execute(DELETE_PASSWORD, (other_user_id, website))
    return {"message": "Password unshared successfully"}, 200

# Logs out a user and clears their session variables (keys)
@app.post("/api/users/<int:user_id>/logout")
def logout(user_id):
    session.clear()
    return {"message": "User logged out"}, 200

# Helper PRNG class used to deterministically generate RSA key pair from master key
class PRNG(object):
    def __init__(self, seed):
        self.index = 0
        self.seed = seed
        self.buffer = b""
    def __call__(self, n):
        while len(self.buffer) < n:
            self.buffer += HMAC.new(
                self.seed + pack("<I", self.index)).digest()
            self.index += 1
        result, self.buffer = self.buffer[:n], self.buffer[n:]
        return result