import sys, os
import MySQLdb

def getConnection():
      mydb = MySQLdb.connect(host="academic-mysql.cc.gatech.edu",user="cs4400_group32",password="AXtzKclB",db="cs4400_group32")
      return mydb
mydb=getConnection()
try:
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM User")
    myresult = mycursor.fetchall()
    
    for x in myresult:
      print(x)
finally:    
    mydb.close()
    
    
    
    
