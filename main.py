import config
import requests
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dbcontrol import password_validation, password_hash


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config.db_url
db = SQLAlchemy(app)
migrate = Migrate(app, db)
API_KEY = config.Api_Key


class User(db.Model):
    __tablename__ = 'userinfo'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    email = db.Column(db.String())
    ages = db.Column(db.Integer())
    password = db.Column(db.LargeBinary)
    firstname = db.Column(db.String())
    lastname = db.Column(db.String())

    def __init__(self, username, email, ages, password, firstname, lastname):
        self.username = username
        self.email = email
        self.ages = ages
        self.password = password
        self.firstname = firstname
        self.lastname = lastname

    def __repr__(self):
        return f"<User {self.username}>"


@app.route("/")
@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        if 'Sign Up' in request.form:
            return redirect(url_for('signup'))
        else:
            user = User.query.filter_by(username=username).first()
            if user and password_validation(password,user.password):
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))
    return render_template('login.html')


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'ages' in request.form and 'password' in request.form and 'firstname' in request.form and 'lastname' in request.form and 'verifypassword' in request.form:
        username = request.form['username']
        email = request.form['email']
        ages = int(request.form['ages'])
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        verifypassword = request.form['verifypassword']
        user = User.query.filter_by(username=username).first()

        if 'Sign Up' in request.form:
            if user and user.username == username:
                return redirect(url_for('signup'))
            else:
                if password!=verifypassword:
                    return redirect(url_for('signup'))
                else:
                    hpass=password_hash(password)
                    user = User(username, email, ages, hpass, firstname, lastname)
                    db.session.add(user)
                    db.session.commit()
                return redirect(url_for('home'))
    return render_template('signup.html')


@app.route("/home", methods=['POST', 'GET'])
def home():
    if 'Profile' in request.form:
        return redirect(url_for('profile'))
    return render_template('home.html')


@app.route("/profile", methods=['POST', 'GET'])
def profile():
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'ages' in request.form and 'password' in request.form and 'firstname' in request.form and 'lastname' in request.form and 'verifypassword' in request.form:
        username = request.form['username']
        email = request.form['email']
        ages = int(request.form['ages'])
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        verifypassword = request.form['verifypassword']
        user = User.query.filter_by(username=username).first()

        if 'Save' in request.form:
            if user and user.username == username:
                return redirect(url_for('profile'))
            else:
                user.email = email
                user.ages = ages
                user.password = password
                user.firstname = firstname
                user.lastname = lastname
                db.session.commit()
                return redirect(url_for('home'))
    return render_template('profile.html')


@app.route("/recipegenerator", methods=['POST', 'GET'])
def recipegenerator():
    return redirect("http://localhost:8501")


def get_random_recipe(number=10):
    url = f'https://api.spoonacular.com/recipes/random?apiKey={API_KEY}&number=100'
    response = requests.get(url)
    if response.status_code == 200:
        recipe_data = response.json()
        return recipe_data['recipes']
    else:
        return []


@app.route("/randomrecipe", methods=['POST', 'GET'])
def randomrecipe():
    recipes = get_random_recipe(number=10)
    return render_template('randomrecipe.html', recipes=recipes)


@app.route("/user", methods=['POST', 'GET'])
def user():
    if request.method == 'GET':
        users = User.query.all()
        results = [
            {
                "username": u.username,
                "email": u.email,
                "ages": u.ages,
                "password": u.password,
                "firstname": u.firstname,
                "lastname": u.lastname
            } for u in users]

        return {"count": len(results), "users": results}


if __name__ == '__main__':
    app.run(debug=True)
