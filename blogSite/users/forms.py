from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from blogSite.models import User

class LoginForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(),Email()])
	password = StringField('Password',validators = [DataRequired()])

class SignupForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(),Email()])
	username = StringField('Username',validators = [DataRequired()])
	password = StringField('Password',validators=[DataRequired()])
	pass_confirm = StringField('Confirm Password',validators=[DataRequired(),EqualTo('password')])

	def check_email(self,field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('This E-mail has already been registered')

	def check_username(self,field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('This Username has already been registered')		

class UpdateUserForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(),Email()])
	username = StringField('Username',validators = [DataRequired()])
	picture = FileField('Update Profile Picture',validators = [FileAllowed(['jpg','png','jpeg'])])
	
	