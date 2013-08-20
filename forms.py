#Building forms for my webapp 

from flask.ext.wtf import Form, TextField, BooleanField, TextAreaField 
#Importing form, text field, t/f field, and multi-text field
from flask.ext.wtf import Required, Length
from models import User
#Importing all the models we need to make forms work 


class LoginForm(Form):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

#the Required import is a validator, a function that can be attached to a field to perform validation on data submitted by the user.
#It checks to make sure the form is not submitted empty.
    
class EditForm(Form):
    nickname = TextField('nickname', validators = [Required()])
    about_me = TextAreaField('about_me', validators = [Length(min = 0, max = 140)])
    
    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname
        
    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname = self.nickname.data).first()
        if user != None:
            self.nickname.errors.append('This nickname is already in use. Please choose another one.')
            return False
        return True
        
class PostForm(Form):
    post = TextField('post', validators = [Required()])
    