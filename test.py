#This is the test file I was working on through the Flask megatutorial as I was going through to build a skeleton for my app and learn things: http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-unit-testing
#This is currently not functioning and has been abandoned since the scope of how I'm building my webapp diverged from the tutorial.

import os 
import unittest #python testing framework "pyunit" 
from datetime import datetime, timedelta #importing datetime and timedela, which expresses diff between two datetimes

import views, models
from models import User, Post


class TestCase(unittest.TestCase):
	def setUp(self):
		app.TESTING = True
		app.csrf_enabled = False
		app.engine = 'sqlite:///' + os.path.join(basedir, 'test.db')
		self.app = app.test_client()
		models.create_al()

	def tearDown(self):
		models.session.remove()
		models.drop_all()

	def test_avatar(self):
		u = User(nickname = 'john', email = 'john@example.com')
		avatar = u.avatar(128)
		expected = 'http://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'
		assert avatar[0:len(expected)] == expected

	def test_make_unique_nickname(self):
		u = User(nickname = 'john', email = 'john@example.com')
		models.session.add(u)
		models.session.commit()
		nickname = User.make_unique_nickname('john')
		assert nickname != 'john'
		u = User(nickname = nickname, email = 'susan@example.com')
		models.session.add(u)
		models.session.commit()
		nickname2 = User.make_unique_nickname('john')
		assert nickname2 != 'john'
		assert nickname2 != nickname

	def test_follow(self):
		# creating four users
		u1 = User(nickname = 'john', email = 'john@example.com')
		u2 = User(nickname = 'susan', email = 'susan@example.com')
		u3 = User(nickname = 'mary', email = 'mary@example.com')
		u4 = User(nickname = 'david', email = 'david@example.com')
		models.ession.add(u1)
		model.add(u2)
		models.session.add(u3)
		models.session.add(u4)
		# making four posts
		utcnow = datetime.utcnow()
		p1 = Post(body = "post from john", author = u1, timestamp = utcnow + timedelta(seconds = 1))
		p2 = Post(body = "post from susan", author = u2, timestamp = utcnow + timedelta(seconds = 2))
		p3 = Post(body = "post from mary", author = u3, timestamp = utcnow + timedelta(seconds = 3))
		p4 = Post(body = "post from david", author = u4, timestamp = utcnow + timedelta(seconds = 4))
		models.session.add(p1)
		models.session.add(p2)
		models.session.add(p3)
		models.session.add(p4)
		models.session.commit()
		# setting up followers
		u1.follow(u1) # john follows himself
		u1.follow(u2) # john follows susan
		u1.follow(u4) # john follows david
		u2.follow(u2) # susan follows herself
		u2.follow(u3) # susan follows mary
		u3.follow(u3) # mary follows herself
		u3.follow(u4) # mary follows david
		u4.follow(u4) # david follows himself
		models.session.add(u1)
		models.session.add(u2)
		models.session.add(u3)
		models.session.add(u4)
		models.session.commit()
		# check the followed posts of each user
		f1 = u1.followed_posts().all()
		f2 = u2.followed_posts().all()
		f3 = u3.followed_posts().all()
		f4 = u4.followed_posts().all()
		assert len(f1) == 3
		assert len(f2) == 2
		assert len(f3) == 2
		assert len(f4) == 1
		assert f1 == [p4, p2, p1]
		assert f2 == [p3, p2]
		assert f3 == [p4, p3]
		assert f4 == [p4]

if __name__ == '__main__':
	unitest.main()