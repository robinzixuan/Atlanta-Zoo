# from LoginDemoApp.database_tables import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from LoginDemoApp.database_tables import load_user


# Classes for wt-forms

class VisitorRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit1 = SubmitField('Sign Up Visitor')
    submit2 = SubmitField('Sign Up Staff')

class StaffRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit2 = SubmitField('Sign Up Staff')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SearchExhibitsForm(FlaskForm):
    name = StringField('Name')
    search = SubmitField('Search')
    num_animal_min = StringField('Min')
    num_animal_max = StringField('Max')
    water_feture = SelectField('Water Feature', choices=[('Yes', 'Yes'),('No', 'No')])
    size_min = StringField('Min')
    size_max = StringField('Max')


class SearchAnimal(FlaskForm):
    name = StringField('Name')
    search = SubmitField('Search')
    species = StringField('Species')
    age_min = StringField('Min')
    age_max = StringField('Max')
    exhibit = SelectField('Exhibit', choices=[('Pacific', 'Pacific'), ('Jungle', 'Jungle'), ('Sahara', 'Sahara'), ('Mountainous','Mountanious')])
    type = SelectField('Type', choices=[('Mammal', 'Mammal'), ('Fish', 'Fish'), ('Amphibian', 'Amphibian'), ('Bird','Bird')])


class SearchShows(FlaskForm):
    name = StringField('Name')
    exhibit = SelectField('Exhibit', choices=[('Pacific', 'Pacific'), ('Jungle', 'Jungle'), ('Sahara', 'Sahara'),
                                              ('Mountainous', 'Mountanious')])
    date = DateField('Date', format = '%m/%d/%Y')
    search = SubmitField('Search')