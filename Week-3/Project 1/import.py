import os, csv, sys;
from flask import Flask
from models import *

app = Flask(__name__)

# Tell Flask what SQLAlchemy databas to use.
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Link the Flask app with the database (no Flask app is actually being run yet).
db.init_app(app)

# def main():
    # Create tables based on each table definition in `models`
# with app.app_context():
#     db.create_all()

def main():
    with app.app_context():
        db.create_all()
        f = open("books.csv")
        reader = csv.reader(f)
        for isbn, title, author, year in reader:
            print(isbn,title,author,year)
            book = Book(isbn=isbn, title=title, author=author, year=year)
            db.session.add(book)
            db.session.commit()
        print("Success", file=sys.stdout)

if __name__ == "__main__":
    main()
    # Allows for command line interaction with Flask application
