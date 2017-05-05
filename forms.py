from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(Form):
	first_name = StringField('First name', validators=[DataRequired("Please enter your first name.")])
	last_name = StringField("Last name", validators=[DataRequired("Please enter your last name")])
	email_unique = StringField('Email', validators=[DataRequired("Please enter your email"), Email("Please use correct email address format")])
	password =PasswordField('Password', validators=[DataRequired("Please enter your password"), Length(min=6, message="Passwords must be longer than 6 characters")])
	submit = SubmitField('Sign up')


class LoginForm(Form):
	email_unique = StringField('Email', validators=[DataRequired("Please enter your email"), Email("Please use correct email address format")])
	password = PasswordField('Password', validators=[DataRequired("Please enter your password"), Length(min=6, message="Passwords must be longer than 6 characters")])
	submit = SubmitField('Login')

class AddressForm(Form):
	address = StringField('Address', validators=[DataRequired("Please enter an address")])
	submit = SubmitField('Search')