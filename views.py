import os
from flask import Flask, render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from flask.ext.openid import OpenID
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from forms import LoginForm, EditForm, PostForm
from models import User, ROLE_USER, ROLE_ADMIN, Post
from datetime import datetime
import models

app = Flask(__name__)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

basedir = os.path.abspath(os.path.dirname(__file__))
oid = OpenID(app, os.path.join(basedir, 'tmp'))

app.csrf_enabled = True
app.secret_key = "rainbowssunshineunicorns2512351"


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

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    models.session.rollback()
    return render_template('500.html'), 500


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        models.session.add(g.user)
        models.session.commit()

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@app.route('/index/<int:page>', methods = ['GET', 'POST'])
@login_required
def index(page = 1):
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body = form.post.data, timestamp = datetime.utcnow(), author = g.user)
        models.session.add(post)
        models.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    posts = g.user.posts
    return render_template('index.html',
        title = 'Home',
        form = form,
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

@app.route('/edit', methods = ['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        models.session.add(g.user)
        models.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html',
        form = form)

#Write out what this does 
@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
        models.session.add(user)
        models.session.commit()
        # have the user follow him/herself
        models.session.add(user.follow(user))
        models.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash('User ' + nickname + ' not found.')
        return redirect(url_for('index'))
    posts = user.posts
    playlists = models.session.query(models.Playlists).filter_by(user_id=g.user.id).all()
    return render_template('user.html',
        user = user,
        posts = posts,
        playlists = playlists)


#functions the follow and unfollow a user
@app.route('/follow/<nickname>')
def follow(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash('User ' + nickname + ' not found.')
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t follow yourself!')
        return redirect(url_for('user', nickname = nickname))
    follow_user = g.user.follow(user)
    if follow_user is None:
        flash('Cannot follow ' + nickname + '.')
        return redirect(url_for('user', nickname = nickname))
    session.add(follow_user)
    session.commit()
    flash('You are now following ' + nickname + '!')
    return redirect(url_for('user', nickname = nickname))

@app.route('/unfollow/<nickname>')
def unfollow(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash('User ' + nickname + ' not found.')
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t unfollow yourself!')
        return redirect(url_for('user', nickname = nickname))
    u = g.user.unfollow(user)
    if u is None:
        flash('Cannot unfollow ' + nickname + '.')
        return redirect(url_for('user', nickname = nickname))
    session.add(u)
    session.commit()
    flash('You have stopped following ' + nickname + '.')
    return redirect(url_for('user', nickname = nickname))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#Page that shows all current playlists and their associated films
@app.route('/playlists')
def show_playlists():
    playlists = models.session.query(models.Playlists).all()
    return render_template('playlists.html', playlists=playlists) 

@app.route('/films')
def show_films():
    all_films = models.session.query(models.Films).all()
    return render_template("films.html",all_films=all_films)
#creating the page to create playlists that shows checkbox input

@app.route('/create_playlist')
def create_playlist():
    select_films = models.session.query(models.Films).all()
    return render_template("create_playlist.html", select_films=select_films)

#adding new playlist name and films to db - > collapse this into create_playlist 
@app.route('/make_playlist')
def make_playlist():
    new_playlist_name = request.args.get("playlist_name")
    added_film = request.args.get("added_film")
    added_playlist = models.Playlists(title=new_playlist_name, user_id=g.user.id)
    models.session.add(added_playlist) 
    models.session.commit()
    models.session.refresh(added_playlist)

    play_order = 0
    for argument in request.args:
        if argument[0:10] == "added_film":
            request.args[argument]
            new_playlist_row = models.Playlist_Entry(playlist_id=added_playlist.id,
                film_id=request.args[argument], play_order=play_order)
            play_order += 1
            models.session.add(new_playlist_row)
    models.session.commit()
    return render_template("playlist_created.html")


@app.teardown_appcontext
def shutdown_session(exception=None):
    models.session.remove()
    


app.run(debug = True)