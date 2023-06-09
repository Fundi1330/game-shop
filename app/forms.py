from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, TextAreaField, IntegerField, MultipleFileField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired
from app.models import User
from flask import flash


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField('Remember ME')
    submit = SubmitField('Sign In')


class RegestrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign In')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            flash('Use a different username')

    def validate_username(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            flash('Use a different email')


class AddGameForm(FlaskForm):
    name = StringField('Game name', validators=[DataRequired()])
    descreption = TextAreaField('Game descreption', validators=[DataRequired()])
    price = IntegerField('Game price', validators=[InputRequired()])
    developer = StringField('Game developer', validators=[DataRequired()])
    publisher = StringField('Game publisher', validators=[DataRequired()])
    release_date = DateField('Game release date', validators=[DataRequired()])
    genre = StringField('Game genre', validators=[DataRequired()])
    images = MultipleFileField('Game images', validators=[DataRequired()])
    submit = SubmitField('Add game')
