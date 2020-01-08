from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import login_user, current_user, logout_user, login_required
from myapp import app, db
from myapp.forms import LoginForm, RegistrationForm, EditProfileForm
from myapp.models import User


# apply this function to all the routes below
# update user's last_seen data automatically
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


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

    # TODO: TASK 4: As a user I can see a confirmation message when I add/delete a todo.
    if form.validate_on_submit():
        user = User(username= form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congrat! you are now a new user of blog')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>') # dynamic component
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404() # if user is not founded, raise 404 error page
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username) # Passing the currnet user's username as argument

    # TODO: TASK 1: As a user I can't add a todo without a description.
    if form.validate_on_submit(): # POST
        if form.about_me.data == "":
            flash("Should fill ABOUT ME")
            return redirect(url_for('edit_profile'))
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('User information Updated')
        return redirect(url_for('user', username=current_user.username))

    elif request.method == "GET": # when user open this page, forms already fill with data of the user
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title="Edit Profile", form=form)
