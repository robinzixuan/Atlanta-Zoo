from flask_table import Table, Col

# from LoginDemoApp import db
#
# cur = db.get_db().cursor()

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


class ExhibitHistoryTable(Table):
    name = Col('Name')
    time = Col('Time')
    num_of_visits = Col('Number of Visits')


class ExhibitDetailTable(Table):
    name = Col('Name')
    species = Col('Species')


class Show:
    def __init__(self, name, time, exhibit):
        self.name = name
        self.time = time
        self.exhibit = exhibit

class ShowsTable(Table):
    name = Col('Name')
    time = Col('Time')
    exhibit = Col('Exhibit')


class ShowHistoryTable(Table):
    name = Col('Name')
    time = Col('Time')
    exhibit = Col('Exhibit')


class StaffShowHistoryTable(Table):
    name = Col('Name')
    time = Col('Time')
    exhibit = Col('Exhibit')


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


class User_info:
    def __init__(self, username, email):
        self.username = username
        self.email = email


class UsersTable(Table):
    username = Col('Username')
    email = Col('Email')


class AnimalCareTable(Table):
    staff_member = Col('Staff Member')
    note = Col('Note')
    time = Col('Time')


class ViewVisitorsTable(Table):
    name = Col('Username')
    email = Col('Email')