import os

from flask import Flask, request, session, render_template
from flask_session import Session
from flask_cors import CORS, cross_origin
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
import psycopg2

# template_folder='../bookexplorer/public/
app = Flask(__name__)
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
CORS(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode='require')
db = scoped_session(sessionmaker(bind=engine))
#CORS(conn)

@app.route("/")
@cross_origin()
def index():
    return "Hello World"

@app.route("/register")
@cross_origin()
def registering():
    username = request.args.get("username")
    password = request.args.get("password")
    #try to add user to database, return fail if unable
    try:
        db.execute("INSERT INTO registered_users (username, password) VALUES (:username, :password)", 
        {"username": username, "password": password})

        db.commit() 

    except exc.SQLAlchemyError:
        return "failure"
    return "success"
