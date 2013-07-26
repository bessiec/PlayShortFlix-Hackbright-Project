CSRF_ENABLED = True
SECRET_KEY = "apocalypsenow12343heartofdarkness"

#CSRF_ENABLED setting activates the cross-site request forgery prevention.
#Secret key is used to create a cryptographic toekn that is used to validate a form.

OPENID_PROVIDERS = [
	{ 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
	{ 'name': 'Yahoo', 'url': 'http://me.yahoo.com' },
	{ 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
	{ 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
	{ 'name': 'MyOpenID', 'url': 'http://www.myopenid.com' }]

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

#The SQLALCHEMY_DATABASE_URI is the path of our database file.
#The SQLALCHEMY_MIGRATE_REPO is the folder in which we will store the SQLAlchemy-migrate data files
