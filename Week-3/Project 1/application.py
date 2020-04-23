import sys, os, time, calendar;
from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from models import *

app = Flask(__name__)

# Tell Flask what SQLAlchemy database to use.
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Link the Flask app with the database (no Flask app is actually being run yet).
db.init_app(app)

# with app.app_context():
#     db.create_all()

@app.route("/", methods=["GET"])
def initial():
    return redirect(url_for('index'))

@app.route("/register", methods=["GET", "POST"])
@app.route("/register/<int:parameter>", methods=["GET", "POST"])
def index(parameter=None):
    if request.method == "POST":
        var1 = request.form.get("email")
        if "." not in var1:
            return render_template("registration_form.html", headline="Please enter valid email address")
        var2 = request.form.get("pwd")
        check = User.query.filter_by(name=var1).first()
        if check is not None:
            return render_template("registration_form.html", headline=var1+" Already Registered. Please Login.")
        user = User(name=var1, password=var2, timestamp=calendar.timegm(time.gmtime()))
        db.session.add(user)
        db.session.commit()
        if len(var1) == 0:
            var1 += "Enter details"
        else:
            var1 += " successfully registered. Please Login."
        return render_template("registration_form.html", headline=var1)
    else:
        variable = ""
        if parameter == 1:
            variable = "You have entered wrong credentials."
        elif parameter == 2:
            variable = "You are not registered. Please Register."
        return render_template("registration_form.html", headline=variable)


@app.route("/admin", methods=["GET"])
def admin():
    users = User.query.order_by(User.timestamp).all()
    names = []
    pwds = []
    timest = []
    for user in users:
        names.append(user.name)
        pwds.append(user.password)
        timest.append(time.ctime(user.timestamp))
    return render_template("registered_users.html", names=names, pwds=pwds, timest=timest, length=len(names))

@app.route("/auth", methods=["POST"])
def authentication():
    mail = request.form.get("email")
    pwd = request.form.get("pwd")
    check = User.query.filter_by(name=mail).first()
    if check is None:
        return redirect(url_for('index', parameter=2))
    if mail == check.name and pwd == check.password:
        if session.get(mail) is None:
            session[mail] = pwd
        return redirect(url_for('func', param=mail))
    else:
        return redirect(url_for('index', parameter=1))

@app.route("/home/<param>", methods=["GET", "POST"])
def func(param):
    if request.method == "GET":
        if session.get(param) is not None:
            return render_template("search.html", headline=param)
        else:
            return "<h1>Please Login to Access</h1>"
    else:
        value = request.form.get('dropdown')
        # print(value, file=sys.stdout) 
        search = request.form.get('box')
        # print(search, file=sys.stdout)
        list = []
        if value == "ISBN":
            list = Book.query.filter(Book.isbn.ilike("%"+search+"%")).all()
        elif value == "Title":
            list = Book.query.filter(Book.title.ilike("%"+search+"%")).all()
        else:
            list = Book.query.filter(Book.author.ilike("%"+search+"%")).all()
        isbns = []
        titles = []
        authors = []
        for i in list:
            isbns.append(i.isbn)
            titles.append(i.title)
            authors.append(i.author)
        return render_template("homepage.html", length=len(list), isbns=isbns, titles=titles, authors=authors, headline=param, search=search)

@app.route("/book/<param>/<arg>", methods=["GET"])
def page(param, arg):
    print(param)
    print(arg)
    return "cool"

@app.route("/logout/<param>", methods=["POST"])
def logout(param):
    session[param] = None
    return redirect(url_for('index'))
