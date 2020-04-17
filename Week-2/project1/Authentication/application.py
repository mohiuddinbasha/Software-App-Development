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

with app.app_context():
    db.create_all()


@app.route("/register", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        var1 = request.form.get("email")
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
        return render_template("registration_form.html", headline="")

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
    # print(variable, file=sys.stdout)
    return render_template("registered_users.html", names=names, pwds=pwds, timest=timest, length=len(names))

@app.route("/auth", methods=["POST"])
def authentication():
    mail = request.form.get("email")
    pwd = request.form.get("pwd")
    check = User.query.filter_by(name=mail).first()
    if check is None:
        return render_template("registration_form.html", headline="You are not registered. Please Register.")
    if mail == check.name and pwd == check.password:
        if session.get("mail") is None:
            session["mail"] = mail
        return render_template("homepage.html", headline=mail)
    else:
        return render_template("registration_form.html", headline="You have entered wrong credentials.")
        # return redirect(url_for('index'), headline="You have entered wrong credentials.")

@app.route("/logout", methods=["POST"])
def logout():
    # if session.get(request.form.get("email")) is not None:
    var = session.get("mail")
    session.clear()
    return redirect(url_for('index'))
    # return render_template("registration_form.html", headline="")
