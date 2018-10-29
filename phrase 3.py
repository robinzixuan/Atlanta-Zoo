import os
import MySQLdb



def opendb():
    db = MySQLdb.connect(host="academic-mysql.cc.gatech.edu",user="cs4400_group32",password="AXtzKclB",db="cs4400_group32" )
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * from User")
        data = cursor.fetchone()
        for i in data:
            print(i)
    except:
         print('Error')
         
            
            
opendb()