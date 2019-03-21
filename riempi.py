import csv
import json
import time
import firebase_admin
import os
from firebase_admin import credentials
from firebase_admin import firestore
from pprint import pprint

def store_file(file):
    with open("./"+file+".txt", newline ="") as filecsv:

        lettore = csv.reader(filecsv, delimiter =",")
        header = next(lettore)

        j = 0

        for campo in lettore:
            doc_ref = db.collection(file).document("0"+str(j))
            if ('ADR' in campo[0] and file != 'calendar_dates' and file != 'shapes') or ('ADR' in campo[2] and ((file == 'calendar_dates') or (file == 'shapes')):
                j = j+1
                i = 0
                doc_ref.set({})
                for valore in header:
                    doc_ref.update({
                            valore: campo[i]
                    })
                    i = i+1

    print(file+" è stato caricato")



#usa un Service Account
cred = credentials.Certificate('./bus-pesaro-firebase-adminsdk-pop87-7ef28ff12c.json')
default_app = firebase_admin.initialize_app(cred)

db = firestore.client()

lista_file = os.listdir('.')
print(lista_file)

for file in os.listdir("."):
    if file.endswith(".txt"):
        ris = file.split(".")
        store_file(ris[0])
