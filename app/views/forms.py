from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,DateField,FloatField
from wtforms.validators import Email,Required,EqualTo

class FlightForm(FlaskForm):
	date_from=DateField('Depart',format="%m/%d/%Y",validators=[Required()])
	date_to=DateField('Return',format="%m/%d/%Y")
	origin=StringField('From',validators=[Required()])
	destination=StringField('To',validators=[Required()])
	target=StringField('Target Price',validators=[Required(),FloatField])
	submit=SubmitField("Submit")
class ForgotForm(FlaskForm):
	email_f = StringField('Email',validators=[Required(),Email()])
	submit = SubmitField('Submit')

class SignUp(FlaskForm):
	email_s = StringField('Email',validators=[Required(),Email()])
	username = StringField('Username',validators=[Required()])
	passw= PasswordField('Password',validators=[Required()])
	passw2 = PasswordField('Confirm Password',validators=[Required(),EqualTo('passw',message="Passwords must match")])
	submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
	email_login=StringField('Email/Username',validators=[Required()])
	passw_login= PasswordField('Password',validators=[Required()])
	submit_login = SubmitField('Login')

class LogoutForm(FlaskForm):
	submit_login=SubmitField("Logout")
