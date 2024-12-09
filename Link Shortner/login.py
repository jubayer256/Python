from flask import session, redirect, render_template
import _md5
from app import db, logged_in


def login(request):
    if logged_in(session):
        return redirect('/dashboard')

    if request.method == "POST":
        form = request.form
        email = form["email"]
        password = _md5.md5(form["password"].encode()).hexdigest()

        cur = db.cursor()
        cur.execute("select fname, id from members where email='{}' and password='{}'".format(email, password))
        authenticate = cur.fetchone()
        db.commit()
        if authenticate:
            session["fname"] = authenticate[0]
            session["id"] = authenticate[1]
            return redirect('/dashboard')
    return render_template('login.html')
