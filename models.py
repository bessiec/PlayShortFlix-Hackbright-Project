from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, SmallInteger, Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from hashlib import md5


engine = create_engine("sqlite:///app.db", echo=True)
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
    about_me = Column(String(140))
    last_seen = Column(DateTime)
    # playlists = relationship('Playlists', backref = 'users.id', lazy = 'dynamic')
    # rating = Column(Integer, unique = False)
    # times_viewed = Column(Integer, unique = False)
    # movies_favorited = Column(Integer, unique = False)
    # bearer_token = Column(String(120), unique = True)
    # twitter = Column(String(120), unique = True)

    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname = nickname).first() == None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname = new_nickname).first() == None:
                break
            version += 1
        return new_nickname


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)
        
    def __repr__(self):
        return '<User %r>' % (self.nickname)    

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True)
    body = Column(String(140))
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)

# class Playlists(Base):
#     __tablename__ = "playlists"

#     id = Column(Integer, primary_key = True)
#     user_id = Column(Integer, ForeignKey('user.id'))
#     multiple_movies = Column(String(140), unique = False)
#     multiple_movies = Column(String(140), unique = False)
#     order_of_plays = Column(Integer, unique = False)
#     playlist_disqus = Column(String(140), unique = False)

    # user = relationship("User",
    #     backref=backref("playlists", order_by=user_id))

# class Movies(Base):
#     id = Column(Integer, primary_key = True)
#     __tablename__ = "movies"
#     url = Column(String(140))
#     link_type = Column(String(140))
#     description = Column(String(140))
#     length = Column(String(140))
#     source = Column(String(140))
#     theme = Column(String(140))
#     festival = Column(String(140))
#     director = Column(String(140))
#     product = Column(String(140))
#     actor = Column(String(140))
#     movie_disqus = Column(String(140))

# # joining
# class Playlist_movies(Base)
#     playlist_id
#     movies_id 
#     order_of_plays

def main():
    """ In case this is needed """
    pass

if __name__ == "__main__":
    main()