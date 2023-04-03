import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

CREATE_USERS_TABLE = (
    "CREATE TABLE IF NOT EXISTS users (user_id SERIAL PRIMARY KEY, name VARCHAR(100) NOT NULL, email VARCHAR(100) NOT NULL UNIQUE, password VARCHAR(100) NOT NULL);"
)

CREATE_PASSWORDS_TABLE = (
    "CREATE TABLE IF NOT EXISTS passwords%s (website TEXT, alias TEXT, passwords TEXT, shared_with_me BOOLEAN, shared_with_others BOOLEAN, shared_list INTEGER[]);"
)

INSERT_USER_RETURN_ID = (
    "INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING user_id;"
)

INSERT_PASSWORDS = (
    "INSERT INTO passwords%s (website, alias, passwords, shared_with_me, shared_with_others, shared_list) VALUES (%s, %s, %s, %s, %s, %s)"
)


@app.route("/api/user", methods = ["GET", "POST"])
def create_users():
    if request.method == "POST":
        data = request.get_json()
        name, email, password = data["name"], data["email"], data["password"]
        print(name)
        print(email)
        print(password)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_USERS_TABLE)
                cursor.execute(INSERT_USER_RETURN_ID, (name, email, password, ))
                user_id = cursor.fetchone()[0]
                cursor.execute(CREATE_PASSWORDS_TABLE, (user_id, ))
        return {"id": user_id, "message": f"Room {name} created."}, 201

@app.route("/api/password", methods = ["POST"])
def create_password():
    if request.method == "POST":
        data = request.get_json()
        user_id, website, alias, password = data["id"], data["website"], data["alias"], data["password"]
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(INSERT_PASSWORDS, (user_id, website, alias, password, "TRUE", "FALSE", f"{{}}", ))
        return {"message": f"Password for {website} inserted"}, 201



# Database: PasswordManager 
# Table 1: Users
#   -> userId
#   -> name
#   -> email
#   -> password
# Table 2: <USERiD>
#   -> website
#   -> alias
#   -> password
#   -> shared_with_me: boolean
#   -> shared_with_others boolean
#   -> shared_list