import mysql.connector

db = mysql.connector.connect(host="localhost", user="root", password="root")

mycursor = db.cursor()

mycursor.execute("show databases")

for i in mycursor:
    print(i)