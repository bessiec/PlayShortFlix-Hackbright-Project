from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, SmallInteger
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

engine = create_engine("sqlite:///ratings.db", echo=True)
session = scoped_session(sessionmaker(bind= engine,
                                        autocommit= False,
                                        autoflush = False))


Base = declarative_base()
Base.query = session.query_property()

ROLE_USER = 0
ROLE_ADMIN = 1


class User(Base):
#users defined on database structure for playshortflix and for Flask megatutorial
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    nickname = Column(String(64), unique = True)
    email = Column(String(120), unique = True)
    role = Column(SmallInteger, default = ROLE_USER)
    posts = relationship('Post', backref = 'author', lazy = 'dynamic')
    playlists = Column(String(120), unique = False)
    rating = Column(Integer, unique = False)
    times_viewed = Column(Integer, unique = False)
    movies_favorited = Column(Integer, unique = False)
    bearer_token = Column(String(120), unique = True)
    twtter = Column(String(120), unique = True)

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True)
    body = Column(String(140), unique = False)
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)

class Playlists(Base):
    __tablename__ = "playlists"

    id = Column(Integer, primary_key = True)
    muliple_movies = Column(Text, unique = False)
    order_of_plays = Column(Integer, unique = False)
    playlist_disqus = Column(Text, unique = False)

class Movies(Base):
    __tablename__ = "movies"
    url = Column(text)
    link_type = Column(text)
    description = Column(text)
    length = Column(text)
    source = Column(text)
    theme = Column(text)
    festival = Column(text)
    director = Column(text)
    product = Column(text)
    actor = Column(text)
    movie_disqus = Column(text)

def main():
    """ In case this is needed """
    pass

if __name__ == "__main__":
    main()