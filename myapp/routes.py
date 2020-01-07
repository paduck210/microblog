from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import login_user, current_user, logout_user, login_required
from myapp import app, db
from myapp.forms import LoginForm, RegistrationForm
from myapp.models import User


@app.route('/')
@app.route('/index')
@login_required # only available with log_in user
def index():
    posts = [
        {
            'author': { 'username' : 'John'},
            'body' : "Harry potter is fun to read, but he has't read it"
        },
        {
            'author': { 'username': 'Mary' },
            'body' : 'My chin condition is not good'
        }
    ]
    return render_template('index.html', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: # already confirmed as a user
        return redirect(url_for('index'))

    form = LoginForm() # Get Login Form

    if form.validate_on_submit(): # On a Filed, when user click submit button
        user = User.query.filter_by(username=form.username.data).first() # get a user instance match with username

        if user is None or not user.check_password(form.password.data):  # is username is incorrect or password is wrong
            flash('Invalid username or password') # show this message on the page
            return redirect(url_for('login')) # and stay on login page

        login_user(user, remember=form.remember_me.data) # after user success to log in
        next_page = request.args.get('next') # user redirect to the page who is supposed to visit
        if not next_page or url_parse(next_page).netloc != '': # get parameter of URL
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # already confirmed as a user
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username= form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congrat! you are now a new user of blog')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



