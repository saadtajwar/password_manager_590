import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

CREATE_USERS_TABLE = (
    "CREATE TABLE IF NOT EXISTS users (userId SERIAL PRIMARY KEY, name TEXT, email TEXT, password TEXT;"
)

CREATE_PASSWORDS_TABLE = (
    "CREATE TABLE IF NOT EXISTS passwords (website TEXT, alias TEXT, password TEXT, shared_with_me BOOLEAN, shared_with_others BOOLEAN, shared_list TEXT[]);"
)

INSERT_USER_RETURN_ID = (
    "INSERT INTO passwords (name, email, password) VALUES (%s %s %s) RETURNING userId;"
)

INSERT_PASSWORDS = (
    "INSERT INTO passwords (website, alias, passwords, shared_with_me, shared_with_others, shared_list) VALUES (%s %s %s %s %s %s)"
)


@app.post("/api/password")
def create_users():
    data = request.get_json()
    name, email, password = data["name"], data["email"], data["password"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(INSERT_USER_RETURN_ID, (name, email, password))
            user_id = cursor.fetchone()[0]
    return {"id": user_id, "message": f"Room {name} created."}, 201




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