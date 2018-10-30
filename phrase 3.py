import os
import MySQLdb
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response


def opendb(db,table):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * from "+table)
        data = cursor.fetchone()
        print('success')
        return data
    except:
         print('Error') 
         
def main():
    db = MySQLdb.connect(host="academic-mysql.cc.gatech.edu",user="cs4400_group32",password="AXtzKclB",db="cs4400_group32" )
    data=opendb(db,"User")
    
    
    db.close()
    
    
    
    
main()