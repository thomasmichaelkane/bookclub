from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from book_club.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=3, max=30)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        
        user = User.query.filter_by(username=username.data).first()
        
        if user is not None:
            raise ValidationError('username taken')
        
    def validate_email(self, email):
        
        user = User.query.filter_by(email=email.data).first()
        
        if user is not None:
            raise ValidationError('email taken')
    
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
class BookForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired()])
    author = StringField('Author')
    # start_reading = BooleanField('I want to start reading this book')
    submit = SubmitField('Search')
    
class ReviewForm(FlaskForm):
    rating = StringField('Rating',
                        validators=[DataRequired()])
    content = StringField('Content',
                          validators=[DataRequired()])
    # start_reading = BooleanField('I want to start reading this book')
    submit = SubmitField('Post')
    
   