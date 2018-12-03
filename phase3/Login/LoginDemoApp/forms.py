# from LoginDemoApp.database_tables import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
from LoginDemoApp import db
# import datetime

from LoginDemoApp.database_tables import load_user

exhibit_choices = [('Pacific', 'Pacific'), ('Jungle', 'Jungle'), ('Sahara', 'Sahara'), ('Mountainous', 'Mountanious'), ("Birds", "Birds")]
type_choices = [('Mammal', 'Mammal'), ('Fish', 'Fish'), ('Amphibian', 'Amphibian'), ('Bird', 'Bird')]
#
# class StaffChoices:
#     staff_choices = []
#
#     @staticmethod
#     def setter(staffs):
#         cls.staff_choices = staffs

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
    animal_min = StringField('Min')
    animal_max = StringField('Max')
    water_feature = SelectField('Water Feature', choices=[('Yes', 'Yes'), ('No', 'No')])
    size_min = StringField('Min')
    size_max = StringField('Max')
    sort = SubmitField('OrderBy')
    direction = SelectField('Direction', choices=[("ASC","ASC"),("DESC","DESC")])
    by = SelectField('By', choices=[("Name", "Name"),("Size", "Size"),("count", "NumAnimals"),("WaterFeature", "is_water")])


class SearchShowHistoryForm(FlaskForm):
    name = StringField('Name')
    exhibit = SelectField('Exhibit', choices=exhibit_choices)
    date = DateTimeField('Datetime', format='%Y-%m-%d %H:%M:%S')
    search = SubmitField('Search Show')
    sort = SubmitField('OrderBy')
    direction = SelectField('Direction', choices=[("ASC","ASC"),("DESC","DESC")])
    by = SelectField('By', choices=[("Name", "Name"),("Time", "Time"),("Exhibit", "Exhibit")])


class AdminViewVisitorForm(FlaskForm):
    sort = SubmitField('OrderBy')
    direction = SelectField('Direction', choices=[("ASC", "ASC"), ("DESC", "DESC")])
    by = SelectField('By', choices=[("Username", "Username"), ("Email", "Email")])

class AdminViewStaffForm(FlaskForm):
    sort = SubmitField('OrderBy')
    direction = SelectField('Direction', choices=[("ASC", "ASC"), ("DESC", "DESC")])
    by = SelectField('By', choices=[("Username", "Username"), ("Email", "Email")])


class SearchExhibitsHistoryForm(FlaskForm):
    name = StringField('Name')
    visit_num_min = StringField('Min')
    visit_num_max = StringField('Max')
    date = DateField('Time', format ='%Y-%m-%d %H:%M:%S')
    search = SubmitField('Search')
    sort = SubmitField('OrderBy')
    direction = SelectField('Direction', choices=[("ASC","ASC"),("DESC","DESC")])
    by = SelectField('By', choices=[("Exhibitname", "Name"), ("Datetime", "Time"), ("c", "Number of Visits")])


class SearchAnimalForm(FlaskForm):
    name = StringField('Name')
    species = StringField('Species')
    age_min = StringField('Min')
    age_max = StringField('Max')
    exhibit = SelectField('Exhibit', choices=exhibit_choices)
    type = SelectField('Type', choices=type_choices)
    search = SubmitField('Search')
    sort = SubmitField('OrderBy')
    direction = SelectField('Direction', choices=[("ASC","ASC"),("DESC","DESC")])
    by = SelectField('By', choices=[("Name", "Name"), ("Species", "Species"), ("Age", "Age"),
                                    ("Place", "Exhibit"),("Type", "Type")])


class AdminSearchAnimalForm(FlaskForm):
    name = StringField('Name')
    species = StringField('Species')
    age_min = StringField('Min')
    age_max = StringField('Max')
    exhibit = SelectField('Exhibit', choices=exhibit_choices)
    type = SelectField('Type', choices=type_choices)
    search = SubmitField('Search')
    remove = SubmitField('Remove')
    sort = SubmitField('OrderBy')
    by = SelectField('By', choices=[("Name", "Name"), ("Species", "Species"), ("Age", "Age"),
                                    ("Exhibit", "Exhibit"), ("Type", "Type")])



class AddAnimalForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    species = StringField('Species', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    exhibit = SelectField('Exhibit', choices=exhibit_choices)
    type = SelectField('Type', choices=type_choices)
    submit = SubmitField('Add animal')




class RemoveForm(FlaskForm):
    remove = SubmitField('Remove')


class AddShowForm(FlaskForm):
    name = StringField('Name')
    exhibit = SelectField('Exhibit', choices=exhibit_choices)
    time = StringField('Time')
    date = DateTimeField('Datetime', format='%Y-%m-%d %H:%M:%S')
    submit = SubmitField('Add Show')
    staff = SelectField('Staff', choices = [])


class StaffSearchShowsForm(FlaskForm):
   sort = SubmitField('OrderBy')
   direction = SelectField('Direction', choices=[("ASC","ASC"),("DESC","DESC")])
   by = SelectField('By', choices=[("Name", "Name"), ("DateAndTime", "Date")])


class SearchShowsForm(FlaskForm):
    name = StringField('Name')
    exhibit = SelectField('Exhibit', choices=exhibit_choices)
    date = DateTimeField('Date', format='%Y-%m-%d %H:%M:%S')
    search = SubmitField('Search')
    log_visit = SubmitField('Log Visit')
    sort = SubmitField('OrderBy')
    direction = SelectField('Direction', choices=[("ASC","ASC"),("DESC","DESC")])
    by = SelectField('By', choices=[("Name", "Name"), ("LocateAt", "Exhibit"), ("DateAndTime", "Time")])


class AdminRemoveShowsForm(FlaskForm):
    name = StringField('Name')
    exhibit = SelectField('Exhibit', choices=exhibit_choices)
    date = DateField('Date', format='%Y-%m-%d %H:%M:%S')
    remove = SubmitField('Remove Show')
    search = SubmitField('Search Show')
    sort = SubmitField('OrderBy')
    direction = SelectField('Direction', choices=[("ASC", "ASC"), ("DESC", "DESC")])
    by = SelectField('By', choices=[("Name", "Name"), ("DateAndTime", "DateAndTime"), ("LocateAt", "Exhibit")])


class ExhibitDetail(FlaskForm):
    name = StringField('Name')
    size = StringField('Size')
    submit = SubmitField('Log Visit')
    num_animals = StringField('Num Animals')
    water_feature = StringField('Water Feature')
    sort = SubmitField('OrderBy')
    direction = SelectField('Direction', choices=[("ASC", "ASC"), ("DESC", "DESC")])
    by = SelectField('By', choices=[("Name", "Name"), ("Species", "Species")])
        #, ("Age", "Age"),("Place", "Exhibit"), ("Type", "Type")])


class AnimalDetail(FlaskForm):
    name = StringField('Name')
    species = StringField('Species')
    age = StringField('Age')
    exhibit = StringField('Exhibit')
    type = StringField('Type')


class AnimalCareForm(FlaskForm):
    Hostby=StringField('Hostby')
    name = StringField('Name')
    species = StringField('Species')
    age = StringField('Age')
    exhibit = StringField('Exhibit')
    type = StringField('Type')
    notes = StringField('Notes')
    log_notes = SubmitField('Log Notes')
    sort = SubmitField('OrderBy')
    direction = SelectField('Direction', choices=[("ASC","ASC"),("DESC","DESC")])
    by = SelectField('By', choices=[("Username", "Staff"),("Texts", "notes"), ("Times", "Date")])

