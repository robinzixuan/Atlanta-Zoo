from flask_table import Table, Col, LinkCol, Col, ButtonCol
from LoginDemoApp import db, login_manager
from flask import render_template, url_for, flash, Markup, redirect, request
from LoginDemoApp.forms import *


class Exhibit:
    def __init__(self, name, size, num_animals, is_water):
        self.name = name
        self.size = size
        self.is_water = is_water
        self.num_animals = num_animals


class ExhibitsTable(Table):
    name = Col('Name')
    size = Col('Size')
    num_animals = Col('NumAnimals')
    is_water = Col('Water')
    choose = LinkCol('Select', 'exhibit_detail', url_kwargs=dict(id='name'))


class Exhibit1:
    def __init__(self, name, species):
        self.name = name
        self.species = species


class ExhibitsTable1(Table):
    name = Col('Name')
    species = Col('Species')
    choose = LinkCol('Select', 'animal_detail',
                     url_kwargs=dict(name='name', species='species'))


class Animal:
    def __init__(self, name, species, exhibit, age, type):
        self.name = name
        self.species = species
        self.exhibit = exhibit
        self.age = age
        self.type = type


class AnimalTable(Table):
    name = Col('Name')
    species = Col('Species')
    exhibit = Col('Exhibit')
    age = Col('Age')
    type = Col('Type')
    choose = LinkCol('Select', 'animal_detail',
                     url_kwargs=dict(name='name', species='species'))


class Show1:
    def __init__(self, name, time, exhibit):
        self.name = name
        self.time = time
        self.exhibit = exhibit


class ShowsTable1(Table):
    name = Col('Name')
    time = Col('Time')
    exhibit = Col('Exhibit')
    choose = LinkCol('SeeExhibit', 'exhibit_detail', url_kwargs=dict(id='exhibit'))


class ExhibitHistoryTable(Table):
    name = Col('Name')
    visit = Col("Number of Visits")
    time = Col('Time')
    choose = LinkCol('Select', 'exhibit_detail', url_kwargs=dict(id='name'))


class ExhibitHistory:
    def __init__(self, name, time, visit):
        self.name = name
        self.visit = visit
        self.time = str(time)


class ShowHistoryTable(Table):
    name = Col('Name')
    time = Col('Time')
    exhibit = Col("Exhibit")


class ShowHistory:
    def __init__(self, name, time, exhibit):
        self.name = name
        self.exhibit = exhibit
        self.time = time


class Animal1:
    def __init__(self, name, species, exhibit, age, type):
        self.name = name
        self.species = species
        self.exhibit = exhibit
        self.age = age
        self.type = type


class AnimalTable1(Table):
    name = Col('Name')
    species = Col('Species')
    exhibit = Col('Exhibit')
    age = Col('Age')
    type = Col('Type')
    choose = LinkCol('Select', 'staff_animal_care', url_kwargs=dict(name='name', species='species'))


class AnimalCareTable(Table):
    name = Col("Staff Member")
    note = Col("Note")
    time = Col('Time')


class AnimalCare:
    def __init__(self, name, time, note):
        self.name = name
        self.note = note
        self.time = str(time)


class Show:
    def __init__(self, name, time, exhibit):
        self.name = name
        self.time = str(time)
        self.exhibit = exhibit


class ShowsTable(Table):
    name = Col('Name')
    time = Col('Time')
    exhibit = Col('Exhibit')
    delete= ButtonCol("Delete","showdelete", url_kwargs=dict(id='name', id1='time') )


# def showdelete(id):
#     cur = db.get_db().cursor()
#     cur.execute(' Delete FROM Shows where Name=%s and DataAndTime=%s', id.name, id.time)


class Animaldelete:
    def __init__(self, name, species, exhibit, age, type):
        self.name = name
        self.species = species
        self.exhibit = exhibit
        self.age = age
        self.type = type

class AnimalTabledelete(Table):
    name = Col('Name')
    species = Col('Species')
    exhibit = Col('Exhibit')
    age = Col('Age')
    type = Col('Type')
    delete= LinkCol("Delete","delete_animal", url_kwargs=dict(id='name',id1='species'))


# def delete_animal(id):
#     cur = db.get_db().cursor()
#     cur.execute(' Delete FROM Animal where Name=%s and Species=%s', id)


class Visitors:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class VisitorsTable(Table):
    name = Col('Username')
    email = Col('Email')
    delete= ButtonCol("Delete","visitordelete", url_kwargs=dict(id='name') )


# def visitordelete():
#     cur = db.get_db().cursor()
#     cur.execute(' Delete FROM Visitor where Username=%s', id)
#     cur.execute('Delete FROM User where Username=%s', id)


class Staffs:
    def __init__(self, name, email):
        self.name = name
        self.email = email


class StaffsTable(Table):
    name = Col('Username')
    email = Col('Email')
    delete= LinkCol("Delete","staffdelete", url_kwargs=dict(id='name'))


# def staffdelete():
#     cur = db.get_db().cursor()
#     cur.execute(' Delete FROM Staff where Username=%s', id)
#     cur.execute('Delete FROM User where Username=%s', id)


class User_info:
    def __init__(self, username, email):
        self.username = username
        self.email = email


class UsersTable(Table):
    username = Col('Username')
    email = Col('Email')
