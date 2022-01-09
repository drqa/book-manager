from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from bookcrud.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', 
                            validators=[DataRequired(),Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                     validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')
 
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError("That username is taken, please choose a different one.")
    
    def validate_email(self, email):
        email = User.query.filter_by(email = email.data).first()
        if email:
            raise ValidationError("That email is taken, please enter a different one.")

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class BookForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    isbn = StringField('ISBN',validators=[DataRequired()])
    pub_year = StringField('Publication Year',validators=[DataRequired()])
    original_lang = StringField('Language',validators=[DataRequired()])
    submit = SubmitField('Submit')

class ShelfCreateForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    description = StringField('Description',validators=[DataRequired()])
    submit = SubmitField('Create Shelf')

class ShelfAddForm(FlaskForm):
    book = StringField('Book Title', validators=[DataRequired()])
    submit = SubmitField('Add Book')

class SearchForm(FlaskForm):
  search = StringField('search', [DataRequired()])
  submit = SubmitField('Search',
                       render_kw={'class': 'btn btn-success btn-block'})



    

