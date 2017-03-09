from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Email,Required,EqualTo
from flask import Flask,render_template,url_for,redirect,flash
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user


app=Flask(__name__)
app.config['SECRET_KEY']='abunchofmaloneybologna'
bootstrap=Bootstrap(app)
app.config['MONGO_DBNAME']='flight_tracker'
mongo = PyMongo(app)

class User():
	def __init__(self,email):
		self.is_active=True
		self.email=email

class ForgotForm(FlaskForm):
	email_f = StringField('Email',validators=[Required(),Email()])
	submit = SubmitField('Submit')

class SignUp(FlaskForm):
	email_s = StringField('Email',validators=[Required(),Email()])
	passw= PasswordField('Password',validators=[Required()])
	passw2 = PasswordField('Confirm Password',validators=[Required(),EqualTo('passw',message="Passwords must match")])
	submit = SubmitField('Submit')

class LoginForm(FlaskForm):
	email_login=StringField('Email',validators=[Required(),Email()])
	passw_login= PasswordField('Password',validators=[Required()])
	submit_login = SubmitField('Login')

@app.route('/',methods=['GET','POST'])
def index():
	email=None
	f_form=ForgotForm()
	s_form=SignUp()
	l_login=LoginForm()
	if l_login.validate_on_submit():
		email_login=l_login.email_login.data
		passw_login=l_login.passw_login.data
		found_user=mongo.db.users.find_one({"email":email_login})
		if found_user is not None and check_password_hash(found_user.get("password"),passw_login):
			print "LOGIN SUCCESS"
			user=User(found_user)
			login_user(user)
			return redirect(url_for(homepage,name=email_login))
		else:
			flash("Invalid User")
	elif f_form.validate_on_submit():
		email=f_form.email_f.data
		f_form.email_f.data=''
	elif s_form.validate_on_submit():
		email=s_form.email_s.data
		passw=s_form.passw.data
		s_form.email_s.data=''
	return render_template('fc.html',f_form=f_form,s_form=s_form,login_form=l_login)

@app.route('/debug')
def home():
	u=mongo.db.user.find()
	for i in u:
		print i.get('name')
	return render_template('main.html')

@app.route('/login')
def homepage(name):
	return render_template('main.html',name=name)


@app.route('/logout')
def logging_out():
	logout_user()
	return redirect(url_for('index'))

if __name__=='__main__':
	app.run(debug=True)
