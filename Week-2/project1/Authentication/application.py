import sys, os, time, calendar;
from flask import Flask, render_template, request
from models import *

app = Flask(__name__)

# Tell Flask what SQLAlchemy database to use.
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Link the Flask app with the database (no Flask app is actually being run yet).
db.init_app(app)

# def main():
    # Create tables based on each table definition in `models`
# print("is it going", file=sys.stdout)
# db.create_all()

# if __name__ == "__main__":
    # Allows for command line interaction with Flask application
with app.app_context():
    db.create_all()


@app.route("/register", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        var1 = request.form.get("email")
        var2 = request.form.get("pwd")
        user = User(name=var1, password=var2, timestamp=calendar.timegm(time.gmtime()))
        db.session.add(user)
        db.session.commit()
        # print(var, file=sys.stdout)
        # print(request.form.get("pwd"), file=sys.stdout)
        if len(var1) == 0:
            var1 += "Enter details"
        else:
            var1 += " successfully registered"
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
