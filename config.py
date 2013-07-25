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