from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Email,Required,EqualTo
from flask import Flask,render_template,url_for,redirect,flash,request
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,UserMixin,LoginManager,login_required
from forms import ForgotForm,SignUp,LoginForm,LogoutForm
from __init__ import *

app=Flask(__name__)
login_manager.init_app(app)
app.config['SECRET_KEY']='abunchofmaloneybologna'
bootstrap=Bootstrap(app)
app.config['MONGO_DBNAME']='flight_tracker'
a=app.app_context()
a.push()
mongo = PyMongo(app)
db=mongo.db
a.pop()

@login_manager.user_loader
def load_user(email):
	a=db.users.find_one({"$or":[{'email':email},{"username":email}]})
	return User(a.get('username')) if a else None
	
class User(UserMixin):
	def __init__(self,email):
		super(User,self).__init__()
		self.id=email
	
@app.route('/',methods=['GET','POST'])
def index():
	email=None
	result,err=None,None
	f_form=ForgotForm()
	s_form=SignUp()
	l_login=LoginForm()
	if l_login.email_login.data and l_login.validate_on_submit():
		result,err=login(l_login)
		l_login.email_login.data=''
		
	elif f_form.email_f.data and  f_form.validate_on_submit():
		result,err=forgot(f_form)
		f_form.email_f.data=''
		
		
	elif s_form.email_s.data and s_form.validate_on_submit():
		result,err=signup(s_form)
		s_form.email_s.data=''
		
	return result if result else render_template('fc.html',f_form=f_form,s_form=s_form,login_form=l_login,error=err)
	
		
def login(l_login):
	email_login=l_login.email_login.data
	passw_login=l_login.passw_login.data
	found_user=db.users.find_one({"$or":[{"email":email_login},{"username":email_login}]})
	result,error=None,None
	if found_user is not None and check_password_hash(found_user.get("password"),passw_login):
		username=found_user.get("username")
		u=User(username)
		login_user(u)
		result=redirect(url_for("homepage",name=username))
	else:
		error="Invalid Username/Password"
	return (result,error)
	
	
def forgot(f_form):
	email=f_form.email_f.data
	result,err=check_and_send(email)
	return result,err

def signup(s_form):
	email=s_form.email_s.data
	passw=s_form.passw.data
	username=s_form.username.data
	found_user=db.users.find_one({ "$or":[{"email":email},{"username":username}]})
	if found_user is None:
		db.users.insert({"email":email,"username":username,"password":generate_password_hash(passw)})
		new_user=User(username)
		login_user(new_user)
		return None,"Account successfully created! Please Login"
	return None,"Email/Username already taken!"

def check_and_send(email):
	rec=db.users.find_one({'email':email})
	if rec:
		#send_email
		return "Email Sent",None
	else:
		return None,"Email not found"

@app.route('/debug')
def home():
	u=mongo.db.user.find()
	for i in u:
		print i.get('name')
	return render_template('main.html')


@app.route('/login',methods=['GET','POST'])
@login_required
def homepage():
	print "Made it to login"
	name=request.args.get('name').capitalize()
	l_out=LogoutForm()
	if l_out.validate_on_submit():
		print("Loggin Out!")
		return redirect(url_for("logging_out"))
	return render_template('main.html',name=name,logoutForm=l_out)


@app.route('/logout')
def logging_out():
	logout_user()
	return redirect(url_for('index'))

if __name__=='__main__':
	app.run(debug=True)
