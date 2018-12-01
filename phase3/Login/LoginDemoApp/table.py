from flask_table import Table, Col
from LoginDemoApp import db, login_manager

class Exhibit:
    def __init__(self, name, size, num_animals, is_water):
        self.name = name
        self.size = size
        self.is_water = is_water
        self.num_animals = num_animals


class ExhibitsTable(Table):
    name = LinkCol('Name','exhibit', url_kwargs=dict(id='id'), attr='name')
    size = Col('Size')
    num_animals = Col('NumAnimals')
    water = Col('Water')

#def exhibit(id):
    
    
class Exhibit1:
    def __init__(self, name, species):
        self.name = name
        self.species = species

    
class ExhibitsTable1(Table):
    name = Col('Name','view_animal',url_kwargs=dict(id='id'), attr='name')
    species = Col('Species')
    log= LinkCol("Log","ExhibitLog", url_kwargs=dict(id='id'), attr='name' )
#def view_animal(id):   
    
#def ExhibitLog(id):


class Animal:
    def __init__(self, name, species, exhibit, age, type):
        self.name = name
        self.species = species
        self.exhibit = exhibit
        self.age = age
        self.type = type

class AnimalTable(Table):
    name = LinkCol('Name','view_exhibit',url_kwargs=dict(id='id'), attr='name')
    species = Col('Species')
    exhibit = Col('Exhibit')
    age = Col('Age')
    type = Col('Type')
    
    
#def view_exihibit(id):
    
class Show1:
    def __init__(self, name, time, exhibit):
        self.name = name
        self.time = time
        self.exhibit = exhibit

class ShowsTable1(Table):
    name = Col('Name')
    time = DatetimeCol('Time')
    exhibit = LinkCol('Exhibit', 'view_exihibit',url_kwargs=dict(id='id'), attr='name' )
    Log= LinkCol("Log","ShowLog",url_kwargs=dict(id='id'), attr='name' )
    
#def ShowLog(id):
  
    

class ExhibithistoryTable(Table):
    name=LinkCol('Name','Log_view',url_kwargs=dict(id='id'), attr='name' )
    visit=Col("Number of Visits")
    time=DatetimeCol('Time')
    
class Exihibithisthory:
    def __init__(self, name, time, visit):
        self.name=name
        self.visit=visit
        self.time=time
        
        
#def Log_view(id):
        


class ShowhistoryTable(Table):
    name=Col('Name')
    time=DatetimeCol('Time')
    exhibit=Col("Exhibit")
    
class Showhisthory:
    def __init__(self, name, time, exhibit):
        self.name=name
        self.exhibit=exhibit
        self.time=time
        
             
    
    
class Show:
    def __init__(self, name, time, exhibit):
        self.name = name
        self.time = time
        self.exhibit = exhibit

class ShowsTable(Table):
    name = Col('Name')
    time = DatetimeCol('Time')
    exhibit = Col('Exhibit')
    delete= LinkCol("Delete","showdelete", url_kwargs=dict(id='id'), attr={'name','time'} )

def showdelete(id):
     cur = db.get_db().cursor()
     cur.execute(' Delete FROM Shows where NAME=%s and DataAndTime=%s',id.name, id.time)


class Animal1:
    def __init__(self, name, species, exhibit, age, type):
        self.name = name
        self.species = species
        self.exhibit = exhibit
        self.age = age
        self.type = type

class AnimalTable1(Table):
    name = LinkCol('Name','animal_care',url_kwargs=dict(id='id'), attr='name' )
    species = Col('Species')
    exhibit = Col('Exhibit')
    age = Col('Age')
    type = Col('Type')

#def animal_care(id):



class AnimalcareTable(Table):
    name=Col("Staff Member")
    note=Col("Note")
    time=DatetimeCol('Time')
    
class Animalcare:
    def __init__(self, name, time, note):
        self.name=name
        self.note=note
        self.time=time
        

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
    delete= LinkCol("Delete","delete_animal", url_kwargs=dict(id='id'), attr='name' )
    
#def delete_animal(id):
    
    
      
    
        
        
class Visitors:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class VisitorsTable(Table):
    name = Col('Username')
    email = Col('Email')
    delete= LinkCol("Delete","visitordelete", url_kwargs=dict(id='id'), attr='name' )

#def visitordelete():
    
    
    
class Staffs:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class StaffsTable(Table):
    name = Col('Username')
    email = Col('Email')
    delete= LinkCol("Delete","staffdelete", url_kwargs=dict(id='id'), attr='name' )

#def staffdelete():
    
    

    



    

    

    
