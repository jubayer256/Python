from app import db, logged_in
from flask import session, render_template, redirect


def dashboard():
    if not logged_in(session):
        return redirect('/login')

    member_id = session["id"]
    cursor = db.cursor()
    cursor.execute("select * from links where member_id='{}'".format(member_id))
    data = cursor.fetchall()
    return render_template('dashboard.html', data=data, count=[len(data), 5000-len(data)])

