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
#login_manager=LoginManager()
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
	a=db.users.find_one({'email':email})['email']
	return User(a)
	
class User(UserMixin):
	def __init__(self,email):
		super(User,self).__init__()
		self.id=email
	
	
	
		
@app.route('/',methods=['GET','POST'])
def index():
	email=None
	f_form=ForgotForm()
	s_form=SignUp()
	l_login=LoginForm()
	if l_login.validate_on_submit():
		return login(l_login)
		
	elif f_form.validate_on_submit():
		return forgot(f_form)
		
	elif s_form.validate_on_submit():
		return signup(s_form)
		
	return render_template('fc.html',f_form=f_form,s_form=s_form,login_form=l_login)
	
	
	
def login(l_login):
	email_login=l_login.email_login.data
	passw_login=l_login.passw_login.data
	found_user=db.users.find_one({"email":email_login})
	print found_user
	if found_user is not None and check_password_hash(found_user.get("password"),passw_login):
		u=User(email_login)
		login_user(u)
		print("Going to homepage")
		return redirect(url_for("homepage",name=email_login))
	else:
		print("Invalid User")
		flash("Invalid User")
	return
	
	
def forgot(f_form):
	email=f_form.email_f.data
	f_form.email_f.data=''
	return

def signup(s_form):
	email=s_form.email_s.data
	passw=s_form.passw.data
	s_form.email_s.data=''
	found_user=db.users.find_one({"email":email})
	print(found_user)
	if found_user is None:
		db.users.insert({"email":email,"password":generate_password_hash(passw)})
		new_user=User(email)
		login_user(new_user)
		print "created User"
		return redirect(url_for(homepage,name=email))
	else:
		print("Email %s already taken!"%(email))
		flash("Email %s already taken!"%(email))
	return

@app.route('/debug')
def home():
	u=mongo.db.user.find()
	for i in u:
		print i.get('name')
	return render_template('main.html')


@app.route('/login',methods=['GET','POST'])
@login_required
def homepage():
	name=request.args.get('name')
	l_out=LogoutForm()
	if l_out.validate_on_submit():
		return redirect(url_for("logging_out"))
	return render_template('main.html',name=name,logoutForm=l_out)


@app.route('/logout')
def logging_out():
	logout_user()
	return redirect(url_for('index'))

if __name__=='__main__':
	app.run(debug=True)
