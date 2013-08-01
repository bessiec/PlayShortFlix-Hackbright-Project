from flask.ext.wtf import Form, TextField, BooleanField, TextAreaField
from flask.ext.wtf import Required, Length

#We imported the Form, TextField, and BooleanField classes that we need 

class LoginForm(Form):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

#the Required import is a validator, a function that can be attached to a field to perform validation on data submitted by the user.
#It checks to make sure the form is not submitted empty.

class EditForm(Form):
    nickname = TextField('nickname', validators = [Required()])
    about_me = TextAreaField('about_me', validators = [Length(min = 0, max = 140)])
