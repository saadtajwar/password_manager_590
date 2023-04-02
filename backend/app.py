from flask import Flask
from datetime import datetime, timezone
import psycopg2
import os


url = os.environ.get("DATABASE_URL")
connection = psycopg2.connect(url)
app = Flask(__name__)

@app.get("/")
def home():
    return "Hello world"


# Post request to add a user to the database
# in data we have the fields "name" "username" and "password"
# Filled out an example of the start of the request which is how you get those fields out of the request
# So now just write a SQL statement to add that to the database with whatever else is needed (if anything else is needed to create a user)
@app.post("/api/users")
def add_user():
    data = request.get_json()
    name = data["name"]
    username = data["username"]
    password = data["password"]


# Get request to get the User with the specified user ID
@app.get("/api/users/<int:user_id>")
def get_user(user_id):
    args = request.args
    # now write a SQL query to retrieve the user based on their ID


# Post reqeust to add the following credential to a user's credential list
@app.post("/api/users/<int:user_id>")
def add_credential(user_id):
    data = request.get_json()
    websiteUsername = data["websiteUsername"]
    credentialUsername = data["credentialUsername"]
    credentialPassword = data["credentialPassword"]
    # now make a new credential with this info and add it to the users list


# TODO: ANY MORE REQUESTS? IDK CANT THINK OF ANYTHING ELSE RN

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