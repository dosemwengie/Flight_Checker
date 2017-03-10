from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Email,Required,EqualTo

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

