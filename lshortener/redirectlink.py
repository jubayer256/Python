from app import db
from flask import redirect


def redirect_link(code):
    cur = db.cursor()
    cur.execute("select original_url from links where shorted_link='{}'".format('lshortneer.herokuapp.com/l/'+code))
    data = cur.fetchone()
    if data:
        return redirect(data[0])
    return redirect('/')
