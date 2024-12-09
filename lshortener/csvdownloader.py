from app import db, logged_in
from flask import session, redirect


def csv():
    if not logged_in(session):
        return redirect('/dashboard')
    cursor = db.cursor()
    cursor.execute("select * from links where member_id={}".format(session['id']))
    data = list(cursor.fetchall())

    print(data)
