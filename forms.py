from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(4, 15)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    gender = SelectField('Gender', choices=[('female', 'Female'), ('male', 'Male'), ('other', 'Other')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
