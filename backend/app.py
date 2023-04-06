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
    "CREATE TABLE IF NOT EXISTS passwords%s (website TEXT, alias TEXT, password TEXT, is_owner BOOLEAN, shared_list INTEGER[]);"
)

GET_USER_ID_WITH_PASSWORD = (
    "SELECT user_id FROM users WHERE email=%s AND password=%s;"
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

INSERT_USER_RETURN_ID = (
    "INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING user_id;"
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
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(INSERT_USER_RETURN_ID, (name, email, password, ))
            user_id = cursor.fetchone()[0]
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
@app.get("/api/users/authenticate")
def authenticate():
    data = request.get_json()
    email, password = data["email"], data["password"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_USER_ID_WITH_PASSWORD, (email, password, ))
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