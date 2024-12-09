from app import db, logged_in
from flask import session, redirect


def delete_link(link_id):
    if not logged_in(session):
        return redirect('/dashboard')

    member_id = session['id']
    cur = db.cursor()
    cur.execute("select 1 from links where id={} and member_id={}"
                .format(link_id, member_id))
    data = cur.fetchone()
    db.commit()
    if data:
        cur.execute("delete from links where id={}".format(link_id))
        db.commit()
        return redirect('/dashboard')
    return redirect('/dashboard')
