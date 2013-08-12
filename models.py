from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, SmallInteger, Text
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from hashlib import md5
import flask.ext.whooshalchemy as whooshalchemy

engine = create_engine("sqlite:///app.db", echo=True)
session = scoped_session(sessionmaker(bind= engine,
                                        autocommit= False,
                                        autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

ROLE_USER = 0
ROLE_ADMIN = 1


followers = Table('user_followers', Base.metadata,
    Column('follower_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('followed_id', Integer, ForeignKey('users.id'), primary_key=True)
)

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
    followed = relationship('User', 
        secondary = followers, 
        primaryjoin = (followers.c.follower_id == id), 
        secondaryjoin = (followers.c.followed_id == id), 
        backref = backref('followers', lazy = 'dynamic'), 
        lazy = 'dynamic')
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

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self
            
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self
            
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        return Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc())


class Post(Base):
    __tablename__ = "posts"
    __searchable__ = ['body']

    id = Column(Integer, primary_key = True)
    body = Column(String(140))
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)


#This association class ties films to playlists and other metadata
class Playlist_Entry(Base): 
    __tablename__ = "playlist_entries"
    
    id = Column(Integer, primary_key = True)
    playlist_id = Column(Integer, ForeignKey('playlists.id'))
    film_id = Column(Integer, ForeignKey('films.id'))
    playlist_name = Column(String(140))
    play_order = Column(Integer, unique = False)
    playlists = relationship('Playlists', backref="playlists_entries", uselist=True)
    films = relationship('Films', backref="playlists_entries", uselist=True)

    # multiple_movies = Column(String(140), unique = False)
    # playlist_disqus = Column(String(140), unique = False)

#making master playlist as parent 
class Playlists(Base):
    __tablename__ = "playlists"
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    # playlist_entries_id = Column(Integer, ForeignKey('playlist_entries.id'))
    # film_id = Column(Integer, ForeignKey('films.id'))
    playlist_entries = relationship('Playlist_Entry')

class Films(Base):
    __tablename__ = "films"
    id = Column(Integer, primary_key = True)
    url = Column(Text)
    title = Column(Text)
    link_type = Column(String(140))
    embed = Column(Text)
    # description = Column(String(140))
    # length = Column(String(140))
    # source = Column(String(140))
    # theme = Column(String(140))
    # festival = Column(String(140))
    # director = Column(String(140))
    # product = Column(String(140))
    # actor = Column(String(140))
    # movie_disqus = Column(String(140))


def main():
    user = User(nickname='bessie', email='oysteromelette@gmail.com')
    playlist1 = Playlists(user_id=user.id)
    arrival = Films(title='The Arrival', url="http://www.youtube.com/watch?v=uQ5TDW_rc7w")
    shanghai_love_market = Films(title='Shanghai Love Market', url='http://www.youtube.com/watch?v=8-NosOJkvNQ')
    parachute_kids = Films(title='Parachute Kids', url='http://www.youtube.com/watch?v=j2F5gaPK6k4')
    seconds_laughter = Films(title="2 Seconds After Laughter", url='http://www.youtube.com/watch?v=j2F5gaPK6k4')
    life = Films(title="I Held My Life in Both Hands", url="http://www.youtube.com/watch?v=5L-uQaDxCnI")
    session.add(user)
    session.add(playlist1)
    session.add(arrival)
    session.add(life)
    session.add(parachute_kids)
    session.add(seconds_laughter)
    session.add(shanghai_love_market)
    session.commit()
    session.refresh(user)
    session.refresh(playlist1)
    session.refresh(arrival)
    session.refresh(shanghai_love_market)


    p1 = Playlist_Entry(playlist_id=playlist1.id, playlist_name="test1", film_id=arrival.id, play_order=1)
    p2 = Playlist_Entry(playlist_id=playlist1.id, playlist_name="test1", film_id=life.id, play_order=2)
    p3 = Playlist_Entry(playlist_id=playlist1.id, playlist_name="test1", film_id=parachute_kids.id, play_order=3)
    p4 = Playlist_Entry(playlist_id=playlist1.id, playlist_name="test1", film_id=seconds_laughter.id, play_order=4)
    p5 = Playlist_Entry(playlist_id=playlist1.id, playlist_name="test1", film_id=shanghai_love_market.id, play_order=5)

    session.add(p1)
    session.add(p2)
    session.add(p3)
    session.add(p4)
    session.add(p5)
    session.commit()



if __name__ == "__main__":
    main()