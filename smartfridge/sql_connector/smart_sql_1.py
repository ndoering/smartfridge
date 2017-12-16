#!/usr/bin/python

import MySQLdb
from datetime import datetime
#import imageio

# Open database connection
db = MySQLdb.connect("localhost","root","","smartfridge" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

#Dropping tables
cursor.execute("DROP TABLE fridgelog")
cursor.execute("DROP TABLE all_fruits")

#Create tables at first
cursor.execute("CREATE TABLE fridgelog (fid INT AUTO_INCREMENT PRIMARY KEY, capturetime TIMESTAMP, full_image LONGBLOB, manual_labeled BOOLEAN, note CHAR(20))")

cursor.execute("CREATE TABLE all_fruits (afid INT NOT NULL AUTO_INCREMENT PRIMARY KEY, fid INT, half_image LONGBLOB, class CHAR(1), confidence FLOAT, prediction FLOAT ,FOREIGN KEY (fid) REFERENCES fridgelog(fid))")

#now = datetime.now()
#Insert values
#Python gibt timestamp
stmt = 'INSERT INTO fridgelog (note) VALUES (%s)'
data = ("hey")
cursor.execute(stmt, data)

#test1
cursor.execute("INSERT INTO fridgelog (note) VALUES ('hey')")

#test2
cursor.execute("INSERT INTO fridgelog (note) VALUES (%s)", ("hey") )

#test3
cursor.execute("INSERT INTO fridgelog VALUES '', (now, NULL, true"))
cursor.execute("INSERT INTO all_fruits")

# disconnect from server
db.close()
