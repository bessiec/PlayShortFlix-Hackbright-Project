from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

# ENGINE = None
# Session = None

engine = create_engine("sqlite:///data.db", echo=True)
session = scoped_session(sessionmaker(bind= engine,
                                        autocommit= False,
                                        autoflush = False))
Base = declarative_base()
Base.query = db_session.query_property()

#declaring classes below 

def init_db():

class User(object):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)

    def __repr__(self):
        return '<User %r>' % (self.nickname)

# app = Flask(__name__)
# app.config.from_object('config')
# db = SQLAlchemy(app)

# from app import views, models

# from app import db

# ROLE_USER = 0
# ROLE_ADMIN = 1



# #fields created as instances of db.Column class, which takes a field type as an argument. 
# #__repr tells Python how to print objects of this class 

