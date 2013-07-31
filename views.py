from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from forms import LoginForm
import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from flask import Flask, render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from models import User, ROLE_USER, ROLE_ADMIN

app = Flask(__name__)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

app.csrf_enabled = True
app.secret_key = "apocalypsenow12343heartofdarkness"

basedir = os.path.abspath(os.path.dirname(__file__))
oid = OpenID(app, os.path.join(basedir, 'tmp'))


#CSRF_ENABLED setting activates the cross-site request forgery prevention.
#Secret key is used to create a cryptographic token that is used to validate a form.

OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'http://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'http://www.myopenid.com' }]

# import os
# basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

#The SQLALCHEMY_DATABASE_URI is the path of our database file.
#The SQLALCHEMY_MIGRATE_REPO is the folder in which we will store the SQLAlchemy-migrate data files



@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
def index():
    user = { 'nickname': 'Miguel' } # fake user
    posts =[
    {
        'author': { 'nickname': 'John' },
        'body': 'Beautiful day in Portland!'
    },
    {
        'author': { 'nickname': 'Susan' },
        'body': 'The Avengers movie was so cool!'
    }
 ]

    return render_template("index.html",
        title = 'Home',
        user = user,
        posts = posts)



@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
    return render_template('login.html', 
        title = 'Sign In',
        form = form,
        providers = OPENID_PROVIDERS)

@app.route('user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash('User ' + nickname + ' not found.')
        return redirect(url_for('index'))
    posts = [
        { 'author': user, 'body': 'HELLO WORLD!' },
        { 'author': user, 'body': "I'm Rick James " }
    ]
    return render_template('user.html',
        user = user.
        posts = posts)

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
        session.add(user)
        session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return direct(url_for('index'))

@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()
    


app.run(debug = True)