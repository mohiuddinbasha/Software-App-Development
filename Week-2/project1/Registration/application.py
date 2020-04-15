import sys
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/register", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        var = request.form.get("email")
        print(var, file=sys.stdout)
        print(request.form.get("pwd"), file=sys.stdout)
        if len(var) == 0:
            var += "Enter details"
        else:
            var += " successfully registered"
        return render_template("form.html", headline=var)
    else:
        return render_template("form.html", headline="")
