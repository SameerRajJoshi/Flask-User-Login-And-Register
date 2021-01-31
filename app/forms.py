from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User

class AdminLogin(FlaskForm):
    username = StringField('Useranme', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message='Password should be at least %(min)d characters long')])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=9, message='Password should be at least %(min)d characters long')],render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6, message='Username Too Short')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=9, message='Password should be at least %(min)d characters long')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Password dont match')])
    accept_tos = BooleanField('I accept Terms & Condition*', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_username(self, useranme):
        user = User.query.filter_by(useranme=username.data).first()
        if user is not None:
            raise ValidationError('Useranme already Taken!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email Already Taken!')


    #for custom validators for username
    def validate_username(self, username):
        excluded_chars = "@*?!'^+%&/()=}][{$#"
        for char in self.username.data:
            if char in excluded_chars:
                raise ValidationError(f"Character {char} is not allowed in username.")
