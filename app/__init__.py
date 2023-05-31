from flask import Flask, render_template, flash, redirect, request, url_for
from app.models import db
from flask_migrate import Migrate

from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from app.forms import RegestrationForm, LoginForm, AddGameForm
from app.models import User, Game

from json import loads, dumps

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
        user = User(username=form.username.data, email=form.email.data, password_hash=form.password.data, cart='')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/cart')
@login_required
def user():
    user = current_user
    cart = user.cart.split(',')
    cart_with_items = []

    for game in cart:
        cart_with_items.append(Game.query.filter_by(name=game).first())

    return render_template('cart.html', title='Cart', user=user, cart=cart_with_items)

@app.route('/game/<gamename>', methods=['GET', 'POST'])
@login_required
def game(gamename):
    game = Game.query.filter_by(name=gamename).first()
    ratings = loads(game.ratings)
    
    if request.method == 'POST':
        if request.form['go'] == 'Add!':
            if not game.name in current_user.cart.split(','):
                current_user.cart += f',{game.name}'
                db.session.commit()
            else:
                flash('Game alredy in cart')
        elif request.form['go'] == 'Write!':
            checkboxes = request.form.getlist('rate')
            data = request.form['message']
            stars = len(checkboxes) + 1
            ratings: list = loads(game.ratings)
            ratings.append({
                "text": data,
                "stars": stars,
                "author": current_user.username
            })
            game.ratings = dumps(ratings)
            db.session.commit()
    
    return render_template('game.html', title=game.name, game=game, ratings=ratings)

@app.route('/games', methods=['GET', 'POST'])
@login_required
def games():
    games_list = Game.query.all()

    developers = []
    
    genres = []

    for game in games_list:
        developers.append(game.developer)
        genres.append(game.genre)

    
    if request.method == 'POST':
        if request.form['filters'] == 'Filter!':
            new_game_list = []
            checkboxes = request.form.getlist('developer')
            for i in games_list:
                if i.developer in checkboxes:
                    new_game_list.append(i)

            return render_template('games.html', title='Games', games_list=new_game_list, developers=set(developers), genres=set(genres))
        elif request.form['filters'] == 'Filter':
            games_sorted = []
            genre_checkboxes = request.form.getlist('genre')
            for j in games_list:
                if j.genre in genre_checkboxes:
                    games_sorted.append(j)
            return render_template('games.html', title='Games', games_list=games_sorted, developers=set(developers), genres=set(genres))
        elif request.form['filters'] == 'Rate!':
            sorted_games = []
            stars_checkboxes = request.form.getlist('stars')
            stars_checkboxes = [int(x) for x in stars_checkboxes]
            for game in games_list:
                for rate in loads(game.ratings):
                    if rate['stars'] in stars_checkboxes:
                        sorted_games.append(game)
            return render_template('games.html', title='Games', games_list=set(sorted_games), developers=set(developers), genres=set(genres))
    return render_template('games.html', title='Games', games_list=games_list, developers=set(developers), genres=set(genres))


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
