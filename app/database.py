from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, SmallInteger, Text
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
	import playshortflix.models
	Base.metadata.create_all(bind = engine)