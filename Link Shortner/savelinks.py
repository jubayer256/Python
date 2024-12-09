from app import db, logged_in
from flask import session, redirect
from hashids import Hashids
import datetime


def add_link(form):
    cursor = db.cursor()
    cursor.execute('select * from links')
    data = cursor.fetchall()
    if not data:
        last_id = 1
    else:
        last_id = data[-1][0]
    h = Hashids(min_length=4, salt="jlf92ifojdf")

    member_id = session['id']
    original_link = form['url']
    if not original_link.startswith("http"):
        original_link = "http://" + original_link
    shorted_link = "lshortneer.herokuapp.com/l/" + h.encode(last_id)
    created_time = datetime.datetime.now()
    clicks = 0
    protected = "None"

    query = """
            insert into links(member_id, original_link, shorted_link, created_time, clicks, protected)
            values('{}', '{}', '{}', '{}', '{}', '{}');
            """.format(member_id, original_link, shorted_link, created_time, clicks, protected)
    cursor.execute(query)
    db.commit()

    return redirect('/dashboard')
