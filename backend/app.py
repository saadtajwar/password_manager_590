import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()

app = Flask(__name__)
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
    "CREATE TABLE IF NOT EXISTS users (user_id SERIAL PRIMARY KEY, name VARCHAR(100) NOT NULL, email VARCHAR(100) NOT NULL UNIQUE, password VARCHAR(100) NOT NULL);"
)

CREATE_PASSWORDS_TABLE = (
    "CREATE TABLE IF NOT EXISTS passwords%s (website TEXT, alias TEXT, passwords TEXT, shared_with_me BOOLEAN, shared_with_others BOOLEAN, shared_list INTEGER[]);"
)

GET_USER_ID = (
    # TODO: Authenticates and gets user_id based on email and password from log in
    "SELECT user_id FROM users WHERE email=%s AND password=%s;"
)

INSERT_USER_RETURN_ID = (
    "INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING user_id;"
)

DELETE_USER_INFO = (
    # TODO: Delete user account given user id, and all associated passwords. This involves a lot of stuff
)

GET_PASSWORDS = (
    "SELECT website, alias, passwords FROM passwords%s;"
)
    
INSERT_PASSWORDS = (
    "INSERT INTO passwords%s (website, alias, passwords, shared_with_me, shared_with_others, shared_list) VALUES (%s, %s, %s, %s, %s, %s)"
)
    
DELETE_PASSWORD = (
    # TODO: Delete a password givne a user_id and password_id
    "DELETE FROM passwords%s WHERE website = %s"
)
    
UPDATE_PASSWORD = (
    "UPDATE passwords%s SET passwords = %s WHERE website = %s;"
)
    
SHARE_PASSWORD = (
    # TODO: Update shared_with_others and shared-list (NON-PRIORITY)
)
    
UNSHARE_PASSWORD = (
    # TODO: Update shared_with_others and shared-list (NON-PRIORITY)
)   

# Registers a user - adds new user to users table and creates their password table
@app.post("/api/users")
def add_user():
    data = request.get_json()
    name, email, password = data["name"], data["email"], data["password"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(INSERT_USER_RETURN_ID, (name, email, password, ))
            user_id = cursor.fetchone()[0]
            cursor.execute(CREATE_PASSWORDS_TABLE, (user_id, ))
    return {"id": user_id, "message": f"User {name} added."}, 201

# Authenticates a user when provided with email and password - returns user's user_id if valid
@app.get("/api/users/authenticate")
def authenticate():
    data = request.get_json()
    email, password = data["email"], data["password"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_USER_ID, (email, password, ))
            user_id = cursor.fetchone()
            if user_id is not None:
                return {"user_id": user_id[0], "message": "Authentication successful"}, 200
            else:
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
            cursor.execute(INSERT_PASSWORDS, (user_id, website, alias, password, "FALSE", "FALSE", f"{{}}", ))
    return {"message": f"Password for {website} inserted"}, 200

# Updates a credential in the user's password table
@app.post("/api/users/<int:user_id>/update")
def update_credential(user_id):
    data = request.get_json()
    website, password = data["website"], data["password"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_PASSWORD, (user_id, password, website))
    return {"message": f"Password for {website} updated"}, 200

# Deletes a credential in the user's password table
@app.post("/api/users/<int:user_id>/delete")
def delete_credential(user_id):
    data = request.get_json()
    website = data["website"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_PASSWORD, (user_id, website))
    return {"message": f"Password for {website} deleted"}, 200