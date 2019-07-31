from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __init__(self,username,email):
        self.username=username
        self.email=email

    def __repr__(self):
        return "<User('%s','%s')>"%(self.username,self.email)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init(self,title,date_posted):
        self.title=title
        self.date_posted=date_posted

    def __repr__(self):
        return "<Post('%s','%s')>"%(self.title,self.date_posted)

class marks(db.Model):
	id =db.Column(db.Integer, primary_key=True)
	Name = db.Column(db.String(15), unique=True,nullable=False)
	physics = db.Column(db.Integer, nullable=False)
	chemistry = db.Column(db.Integer, nullable=False)
	maths = db.Column(db.Integer, nullable=False)

	def __init__(self,Name,physics,chemistry,maths):
		self.Name = Name
		self.physics = physics
		self.chemistry = chemistry
		self.maths = maths
	def __repr__(self):
		return "<marks ('%s','%d','%d','%d')>"%(self.Name,self.physics,self.chemistry,self.maths)

