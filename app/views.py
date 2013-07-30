from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import render_template, flash, redirect
from app import app
from forms import LoginForm
from app import model
import os
from flask.ext.login import LoginManager
from flask.ext.openid import openid
from config import basedir


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
oid = OPENID(app.os.path.join(basedir, 'tmp'))

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
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + 
            str(form.remember_me.data))
        return redirect('/')
    return render_template('login.html', 
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

#Above has imported LoginForm class, instatiated an object from it, and sent it down to the template.
#The methods argument tells Flask that this view function accepts GET and POST requests.  Without it, it would only accept GET requests.
#The users will be using POST requests, so we want to accept those.
#The validate on submit method does all the form processing work.  If it fails to validate, the function will return false to prompt user to correct.
#The flash function is a quick way to show a message on the next page presented to a user. 

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
    

from app import app
app.run(debug = True)