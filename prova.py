import csv
import json
import time
import os
import mysql.connector
from pprint import pprint

def store_file(file):
    with open("./"+file+".txt", newline="") as filecsv:

        lettore = csv.reader(filecsv, delimiter =",")
        header = next(lettore)

        mycursor.execute("CREATE TABLE IF NOT EXISTS "+file+"(id INT PRIMARY KEY)")
        #mycursor.execute("ALTER TABLE "+file+" ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")

        j = 0
        for riga in lettore:
            i = 0
            app = header

            mycursor.execute("INSERT INTO "+file+" (id) VALUES ("+str(j+1)+")")
            for valore in app:
                if j == 0:
                    mycursor.execute("ALTER TABLE "+file+" ADD COLUMN "+valore+" VARCHAR(64)")
                sql ="UPDATE "+file+" SET "+valore+" = '{0}'".format(riga[i])+" WHERE id = "+str(j+1)+""
                print(sql)
                #val = riga[i]
                val = "GGG"
                mycursor.execute(sql)
                cnx.commit()
                i = i+1

            j = j+1



cnx = mysql.connector.connect(user='root', password='doremi666', host='localhost', database='mydb')
mycursor = cnx.cursor()

for file in os.listdir("."):
    if file.endswith(".txt"):
        ris = file.split(".")
        store_file(ris[0])



cnx.close()
