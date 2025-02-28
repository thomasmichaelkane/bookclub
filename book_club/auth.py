from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

from book_club.models import User
from book_club.forms import RegistrationForm, LoginForm
from book_club.genesis import create_user
from book_club import db, bcrypt

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        create_user(form=form)
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, remember=True)
        
        flash(f'account created for {form.username.data}', category='success')
        return redirect(url_for('views.home'))
    
    return render_template('register.html', title='Sign Up', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Logged in {user.username}', category='success')
            return redirect(url_for('views.home'))
        
        else:
            flash(f'Failed login', category='danger')
            
    return render_template('login.html', title='Login', form=form)
    
@auth.route('/logout') 
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login')) 

@auth.route('/account') 
@login_required
def account():
    return render_template('account.html', title='My Account')#, form=form)
