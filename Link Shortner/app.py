from flask import Flask, render_template, session, request, redirect
import database

app = Flask(__name__)
app.secret_key = 'jflkjoi3u8owjfis'
db = database.connect()  # connect to database


def logged_in(s):
    if s.get("fname"):
        return True
    else:
        return False


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login_user():
    import login
    return login.login(request)


@app.route('/logout')
def logout_user():
    session.clear()
    return redirect('/login')


@app.route('/signup', methods=["GET", "POST"])
def signup_user():
    import signup
    return signup.signup(request)


@app.route('/dashboard')
def dashboard_user():
    import dashboard
    return dashboard.dashboard()


@app.route("/add-links", methods=["POST"])
def add_links():
    import savelinks
    return savelinks.add_link(request.form)


@app.route("/delete-link/<link_id>")
def delete_link(link_id):
    import deletelink
    return deletelink.delete_link(link_id)


@app.route("/l/<code>")
def redirect_link(code):
    import redirectlink
    return redirectlink.redirect_link(code)


if __name__ == '__main__':
    app.run(debug=False)
