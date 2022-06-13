from flask import Flask, url_for, request, session, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import random


def generateSecretKey() -> str:
    key = ''
    for i in range(25):
        key = key + str(random.choice(range(10)))
    return key


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = generateSecretKey()
app.permanent_session_lifetime = timedelta(minutes=2)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.column(db.Integer, primary_key=True)
    username = db.Column(db.Sting(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<User {self.id}>'


@app.route('/', methods=['POST', 'GET'])
@app.route('/log_in', methods=['POST', 'GET'])
def log_in():
    if request.method == 'POST':
        session['email'] = request.form['email']
        session['password'] = request.form['password']
        return redirect('/log_in/check')
    return render_template('log_in.html')


@app.route('/registration', methods=["POST", "GET"])
def registration():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']

        if password == confirm:
            user = User(
                username=username,
                email=email,
                password=password
            )
        try:
            db.session.add(user)
            db.session.commit()
            return render_template(url_for('log_in'))
        except:
            return "you can't register"
        return render_template('registration.html')


@app.route("/profile")
def profile():
    if 'user' in session:
        return render_template("profile.html")
    return redirect(url_for("log_in"))


@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop("user", None)
    return redirect('/log_in')


if __name__ == '__main__':
    app.run()
