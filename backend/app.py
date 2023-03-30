from flask import Flask

app = Flask(__name__)

@app.get("/")
def home():
    return "Hello world"


# Database: PasswordManager 
# Table 1: Users
#   -> userId
#   -> name
#   -> email
#   -> password
# Table 2: <USERiD>
#   ->  website
#   -> alias
#   -> password
#   -> shared_with_me (bool)
#   -> shared_with_others (bool)
#   -> shared_list