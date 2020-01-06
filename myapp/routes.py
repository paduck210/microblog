from myapp import app
from flask import render_template
from myapp.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = { 'username': 'paduck' }
    title = "Home"
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
    return render_template('index.html', title = title, user=user, posts=posts)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)