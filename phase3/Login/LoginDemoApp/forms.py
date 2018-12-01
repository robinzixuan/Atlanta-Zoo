# from LoginDemoApp.database_tables import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_table import Table, Col
from wtforms.fields.html5 import DateField
import LoginDemoApp.main as main

staff_choice = []
staff_list = main.get_staff_name()
for entry in staff_list:
    staff_choice.append((entry, entry))
# Classes for wt-forms

class VisitorRegistrationForm(FlaskForm):
    # First param of input field is id and kwargs are used for input validation
    # DataRequired just checks that the input field is not submitted empty
    # Length() checks input length
    # Email() check if input is an email address
    # EqualTo() checks if input is equal to another specified input field
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit1 = SubmitField('Sign Up')
    submit2 = SubmitField('Sign Up')

    # # Add custom validation (check if username and email are already stored in database)
    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user:
    #         raise ValidationError('That username is taken. Please choose a different one.')
    #
    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user:
    #         raise ValidationError('That email is taken. Please choose a different one.')
class StaffRegistrationForm(FlaskForm):
    # First param of input field is id and kwargs are used for input validation
    # DataRequired just checks that the input field is not submitted empty
    # Length() checks input length
    # Email() check if input is an email address
    # EqualTo() checks if input is equal to another specified input field
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit2 = SubmitField('Sign Up')

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


class ExhibitsTable(Table):
    name = Col('Name')
    size = Col('Size')
    num_animals = Col('NumAnimals')
    water = Col('Water')


class ShowsTable(Table):
    name = Col('Name')
    time = Col('Time')
    exhibit = Col('Exhibit')


class SearchAnimal(FlaskForm):
    name = StringField('Name')
    search = SubmitField('Search')
    species = StringField('Species')
    age_min = StringField('Min')
    age_max = StringField('Max')
    exhibit = SelectField('Exhibit', choices=[('Pacific', 'Pacific'), ('Jungle', 'Jungle'), ('Sahara', 'Sahara'), ('Mountainous','Mountanious')])
    type = SelectField('Type', choices=[('Mammal', 'Mammal'), ('Fish', 'Fish'), ('Amphibian', 'Amphibian'), ('Bird','Bird')])


class AnimalTable(Table):
    name = Col('Name')
    species = Col('Species')
    exhibit = Col('Exhibit')
    age = Col('Age')
    type = Col('Type')


class SearchShows(FlaskForm):
    name = StringField('Name')
    exhibit = SelectField('Exhibit', choices=[('Pacific', 'Pacific'), ('Jungle', 'Jungle'), ('Sahara', 'Sahara'),
                                              ('Mountainous', 'Mountanious')])
    date = DateField('Date', format = '%m/%d/%Y')
    search = SubmitField('Search')


class ShowHistoryTable(Table):
    name = Col('Name')
    time = Col('Time')
    exhibit = Col('Exhibit')


class StaffFunction(FlaskForm):
    search_animal = SubmitField('Search Animal')
    view_shows = SubmitField('View Shows')
    log_out = SubmitField('Log Out')


class VisitorFunction(FlaskForm):
    search_animal = SubmitField('Search for Animals')
    search_show = SubmitField('Search Shows')
    search_exhibit = SubmitField('Search Exhibits')
    view_ex_his = SubmitField('View Exhibit History')
    view_show_his = SubmitField('View Show History')
    log_out = SubmitField('Log Out')


class AdminFunctio(FlaskForm):
    view_visitor = SubmitField('View Visitor')
    view_staff = SubmitField('View Staff')
    view_show = SubmitField('View Shows')
    view_animal = SubmitField('View Animal')
    add_show = SubmitField('Add Show')
    log_out = SubmitField('Log Out')


class AddAnimal(FlaskForm):
    name = StringField('Name')
    exhibit = SelectField('Exhibit', choices=[('Pacific', 'Pacific'), ('Jungle', 'Jungle'), ('Sahara', 'Sahara'),
                                              ('Mountainous', 'Mountanious')])
    date = DateField('Date', format='%m/%d/%Y')
    time = StringField('Time')
    add_animal = SubmitField('Add Animal')
    species = StringField('Species')
    staff = SelectField('Staff', choices=staff_choice)



class AddShows(FlaskForm):
    name = StringField('Name')
    exhibit = SelectField('Exhibit', choices=[('Pacific', 'Pacific'), ('Jungle', 'Jungle'), ('Sahara', 'Sahara'),
                                              ('Mountainous', 'Mountanious')])
    date = DateField('Date', format='%m/%d/%Y')




