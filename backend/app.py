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

GET_USER_INFO = (
    # TODO: Authenticates and gets user_id based on email and password from log in
    # SELECT column_name FROM information_schema.columns WHERE table_name='your_table' and column_name='your_column';
    "SELECT %s FROM information_schema.columns WHERE table_name='%s' and column_name='%s';"
)

INSERT_USER_RETURN_ID = (
    "INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING user_id;"
)

DELETE_USER_INFO = (
    # TODO: Delete user account given user id, and all associated passwords. This involves a lot of stuff
)

GET_PASSWORDS = (
    # TODO: Get's all the passwords given a user_id
)
    
INSERT_PASSWORDS = (
    "INSERT INTO passwords%s (website, alias, passwords, shared_with_me, shared_with_others, shared_list) VALUES (%s, %s, %s, %s, %s, %s)"
)
    
DELETE_PASSWORD = (
    # TODO: Delete a password givne a user_id and password_id
)
    
UPDATE_PASSWORD = (
    # TODO: Update website, alias, or password field
)
    
SHARE_PASSWORD = (
    # TODO: Update shared_with_others and shared-list (NON-PRIORITY)
)
    
UNSHARE_PASSWORD = (
    # TODO: Update shared_with_others and shared-list (NON-PRIORITY)
)   

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

@app.get("/api/users/authenticate")
def authenticate():
    # TODO authenticate user and return user_id
    data = request.get_json()
    email, password = data["email"], data["password"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_USER_INFO, (email, "users", "email", ))
            user_info = cursor.fetchone()[0]
            # if len(user_info) > 1 and user_info["password"] == password
    return {"user_info": user_info, "message": f"User info with email {email} was retrieved"}, 201

@app.get("/api/users/<int:user_id>")
def get_user(user_id):
    # TODO return users passwords based on IDs, eventually implement API endpoint security
    pass

@app.post("/api/users/<int:user_id>")
def add_credential(user_id):
    data = request.get_json()
    website, alias, password =  data["website"], data["credentialUsername"], data["credentialPassword"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_PASSWORDS, (user_id, website, alias, password, "FALSE", "FALSE", f"{{}}", ))
    return {"message": f"Password for {website} inserted"}, 201