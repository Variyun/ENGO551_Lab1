import csv
import os

from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    # see if table exists in database, if not create table or drop exisiting table
    try:
        db.execute("SELECT 1 FROM library LIMIT 1")
        db.execute("DROP TABLE library")
        db.execute("CREATE TABLE library (isbn varchar, title varchar, author varchar, year int)")
        db.commit()
    except exc.SQLAlchemyError:
        db.execute("CREATE TABLE library (isbn varchar, title varchar, author varchar, year int)")
        db.commit()
    # open csv
    f = open("books.csv")
    reader = csv.reader(f)
    # store books in database 
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO library (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                    {"isbn": isbn, "title": title, "author": author, "year": year})
    db.commit()
    print("Finished importing books")

if __name__ == "__main__":
    main()
