from flask import render_template, url_for, flash, redirect, request,g
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post,marks
from flask_login import login_user, current_user, logout_user, login_required


'''@app.before_request
def before_request():
	try:
		g.conn=db1.connect("localhost","root","root123",'student')
	except:
		g.conn=db1.connect("localhost","root","root123")
		curr= g.conn.cursor()
		curr.execute("CREATE DATABASE IF NOT EXISTS student")
	finally:
		g.conn=db1.connect("localhost","root","root123",'student')
		curr= g.conn.cursor()
		#curr.execute("CREATE TABLE IF NOT EXISTS marks (ID INT AUTO_INCREMENT PRIMARY KEY,Name VARCHAR(15),physics INT(3),chemistry INT(3),maths INT(3))")


@app.after_request
def after_request(response):
	if g.conn is not None:
		g.conn.close()
	return response
'''

posts = [
    {
        'author': 'KB Patil',
        'title': 'Student Result',
        'content': 'First post content',
        'date_posted': 'june 28, 2019'
    }
]


@app.route("/")
@app.route("/home")
def home():
    db.create_all()
    return render_template('home.html', posts=posts)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/student')
@login_required
def student():
	return render_template('student.html')


@app.route('/result',methods = ['POST', 'GET'])
@login_required
def result():
	error=None
	if request.method == 'POST':
		user = marks.query.filter_by(Name=request.form['Name']).first()
		if user:
			flash('Student details already present!')
			return redirect(url_for('student'))

		else:
			user = marks(Name = request.form['Name'], physics = request.form['Physics'], chemistry = request.form['chemistry'], maths = request.form['Mathematics'])
			db.session.add(user)
			db.session.commit()	
			return render_template('result.html',result=marks.query.all())
	else:
		return render_template('result.html',result=marks.query.all())
	

@app.route('/edit/<int:slno>')
@login_required
def edit(slno):
	x = marks.query.filter_by(id=slno).first()
	return render_template('edit.html',x=x)

@app.route('/update/<int:slno>',methods=['POST','GET'])
@login_required
def update(slno):
	if request.method == 'POST':
		marks.query.filter_by(id=slno).update(dict(physics = request.form["Physics"], chemistry = request.form["chemistry"], maths = request.form["Mathematics"]))
		db.session.commit()
		return redirect(url_for('result'))
		
@app.route('/delete/<int:slno>')
@login_required
def delete(slno):
	x =marks.query.filter_by(id=slno).first()
	db.session.delete(x)
	db.session.commit()
	return redirect(url_for('result'))

