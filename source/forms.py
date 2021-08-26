from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Email,EqualTo, ValidationError
from source.models import User


class RegisterForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('password',validators=[DataRequired(),EqualTo('confirm')])
    confirm=PasswordField('confirm_password',validators=[DataRequired()])
    submit=SubmitField('Signup')

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered')


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('connect')

class PostForm(FlaskForm):
    category=SelectField('category',choices=[('KGISl','Technology'),('KGH','Hospital'),('KGC','Cinemas')])
    cat_fields=SelectField('fields',choices=[('ML','machine learning'),('web','web devolopment')])
    submit=SubmitField('Post')