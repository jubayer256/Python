from app import db, logged_in
import _md5
from flask import session, redirect, render_template


def signup(request):
    if logged_in(session):
        return redirect('/dashboard')
    if request.method == "POST":
        form = request.form
        fname = form["fname"]
        lname = form["lname"]
        email = form["email"]
        password = form["password1"]
        enc_pass = _md5.md5(password.encode()).hexdigest()
        query = """
                    insert into members(fname, lname, email, password)
                    values('{}', '{}', '{}', '{}');
                    """.format(fname, lname, email, enc_pass)
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()

        return "Signup successful. Continue to login page"
    return render_template("signup.html")
