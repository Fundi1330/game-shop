from flask import Flask, render_template, flash, redirect, request, url_for
from app.models import db
from flask_migrate import Migrate

from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from app.forms import RegestrationForm, LoginForm, AddGameForm
from app.models import User, Game

app = Flask(__name__)
app.config["SECRET_KEY"] = '1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.app_context().push()

db.init_app(app)
migrate = Migrate(app, db)

login = LoginManager(app)



"""Декоратори для відображення сторінок та їх вмісту"""
with app.app_context():
    db.create_all()

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
@app.route('/index/')
def index():
    authenticated = True
    if current_user.is_authenticated:
        authenticated = False
    return render_template('index.html', title='Home', authenticated=authenticated)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
       return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Incorrect login data: check password or username")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("index"))
    
    return render_template("login.html", title="Sign in", form=form)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegestrationForm()
    if form.validate_on_submit():
        flash("Congrats!")
        user = User(username=form.username.data, email=form.email.data, password_hash=form.password.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/cart/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('cart.html', title='Cart', user=user)

@app.route('/game/<gamename>')
@login_required
def game(gamename):
    game = Game.query.filter_by(name=gamename).first()
    
    
    return render_template('game.html', title=game.name, game=game)

@app.route('/games')
@login_required
def games():
    games_list = Game.query.all()
    return render_template('games.html', title='Game', games_list=games_list)


@app.route('/add_game', methods=["GET", "POST"])
def add_good():
    form = AddGameForm()
    if form.validate_on_submit():
        flash('Game succefully added to DataBase')
        game = Game(name=form.name.data, descreption=form.descreption.data, price=form.price.data,
                     developer=form.developer.data, publisher=form.publisher.data, release_date=form.release_date.data)
            

        db.session.add(game)
        db.session.commit()
    return render_template('add_game.html', title='Add game', form=form)