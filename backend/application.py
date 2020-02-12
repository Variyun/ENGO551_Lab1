import os, psycopg2, requests
from flask import Flask, request, session, render_template, jsonify
from flask_session import Session
from flask_cors import CORS, cross_origin
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker

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

# default app address 
@app.route("/")
@cross_origin()
def index():
    return "Hello World"

# registration for users
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

# check for username, return error if username exists 
@app.route("/namecheck")
@cross_origin()
def namecheck():
    username = request.args.get("username")
    if db.execute("SELECT username FROM registered_users WHERE username=:username", {"username": username}).rowcount == 1:
        return ({"user": username, "exists": "true"})
    else:
        return ({"exists": "false"}) 

# See if username and password match in database to log in user 
@app.route("/loggingin")
@cross_origin()
def loggingin():
    username = request.args.get("username")
    password = request.args.get("password")
    if db.execute("SELECT username FROM registered_users WHERE username=:username AND password=:password", {"username": username, "password": password}).rowcount == 1:
        return ({"user": username, "loggedin": "true"})
    else:
        return ({"user": username, "loggedin": "false"}) 

@app.route("/booksearch")
@cross_origin()
def booksearch():
    book = request.args.get("book")
    option = request.args.get("option")
    if option == "Author":
        out_book = db.execute("SELECT * FROM library WHERE author LIKE :book", {"book": "%" + book + "%"}).fetchall()
        data = jsonify({'result': [dict(row) for row in out_book]})
        return data
    elif option == "Title":
        out_book = db.execute("SELECT * FROM library WHERE title LIKE :book", {"book": "%" + book + "%"}).fetchall()
        data = jsonify({'result': [dict(row) for row in out_book]})
        return data
    elif option == "Year":
        out_book = db.execute("SELECT * FROM library WHERE CAST(year as TEXT) LIKE :book", {"book": "%" + book + "%"}).fetchall()
        data = jsonify({'result': [dict(row) for row in out_book]})
        return data
    elif option == "ISBN":
        out_book = db.execute("SELECT * FROM library WHERE isbn LIKE :book", {"book":"%" + book + "%"}).fetchall()
        data = jsonify({'result': [dict(row) for row in out_book]})
        return data

@app.route("/goodread")
@cross_origin()
def goodread():
    # key = "swIxMzw2BAh2FK5fXd3PSg"
    url = "https://www.goodreads.com/book/review_counts?key=swIxMzw2BAh2FK5fXd3PSg&isbns="
    isbns = request.args.get("isbn")
    test = url + isbns + "&format=json"
    r = requests.get(url + isbns + "&format=json")
    if r.ok:
        return jsonify({"goodread": r.json(), "status": "good"}) 
    else:
        return jsonify({"status": "bad"}) 

@app.route("/submitreview")
@cross_origin()
def submitreview():
    isbn = request.args.get("isbn")
    username = request.args.get("username")
    review = request.args.get("review")
    rating = request.args.get("rating")
    try:
        db.execute("INSERT INTO reviews (isbn, username, review, rating) VALUES (:isbn, :username, :review, :rating)", 
        {"isbn": isbn, "username": username, "review": review, "rating": rating})
        db.commit() 
    except exc.SQLAlchemyError:
        return "failure"
    return "success"

@app.route("/get_review")
@cross_origin()
def get_review():
    isbn = request.args.get("isbn")
    out_book = db.execute("SELECT * FROM reviews WHERE isbn=:isbn", {"isbn": isbn}).fetchall()
    data = jsonify({'result': [dict(row) for row in out_book]})
    return data

# Api function for other users to use 
@app.route("/api", methods=["GET"])
@cross_origin()
def api():
    isbn = request.args.get("isbn")
    book = db.execute("SELECT * FROM library WHERE isbn=:isbn", {"isbn": isbn}).fetchall()
    if len(book) == 0:
        return "404: Could not find book with this ISBN"
    try: # get ratings
        reviews = db.execute("SELECT rating FROM reviews WHERE isbn=:isbn", {"isbn": isbn}).fetchall()
    except exc.SQLAlchemyError:
        return "Error with SQL"

    # calculate average ratings/ score
    avg = 0
    if len(reviews) != 0:
        for row in reviews:
            avg = avg + row.rating
        avg = avg / len(reviews)
    return jsonify(title=book[0].title, author=book[0].author, year=book[0].year, isbn=isbn, review_count=len(reviews), average_score=avg)
 
    
    