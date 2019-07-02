import telepot
import csv
import math
from config import TOKEN, API_KEY, URL_EXTRAURBANE, URL_URBANE
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
import bs4 as bs
import urllib.request
import json
from pprint import pprint
import time
from apiclient.discovery import build
import requests
import gmaps
import time
import os
import request
import mysql.connector
from emoji import emojize




class MessageHandler:
    # Preserve all different user stages between messages
    USER_STATE = {}
    lista_costi = []
    lista_descrizione = []
    count = 0
    count2 = 0
    myresult = []

    def handle(self, msg):

        content_type, chat_type, chat_id = telepot.glance(msg)

        keyboardd = InlineKeyboardMarkup(inline_keyboard=[
                         [InlineKeyboardButton(text='Yes', callback_data='yes'),
                         InlineKeyboardButton(text='No', callback_data='no')],
                     ])
        try:
            self.USER_STATE[chat_id]
        except KeyError:
            self.USER_STATE[chat_id] = 0

        if content_type == "text":
            msgg = json.dumps(msg, indent=4)
            input_msg = msg['text']
            print(msgg)
            # Check user state
            print(self.USER_STATE[chat_id])


            if ((input_msg == "/inizia")  or (self.USER_STATE[chat_id] == 0) or (input_msg == "HOME") or (input_msg == "/HOME")):
                self.send_options(chat_id)



            elif input_msg == "/start" and \
                self.USER_STATE[chat_id] == 0:
                bot.sendMessage(chat_id, "Benvenuto "+msg['chat']['first_name']+" questo bot ti aiuterà a scegliere il tragitto che più è adatto a te")

            elif input_msg == "Linea" and \
                self.USER_STATE[chat_id] == 1:
                bot.sendMessage(chat_id, 'Digita la linea che vuoi cercare...', reply_markup=ReplyKeyboardRemove())
                self.USER_STATE[chat_id] = 2

            elif (self.USER_STATE[chat_id] == 2 or self.USER_STATE[chat_id] == 5) and input_msg != "/other":
                bot.sendMessage(chat_id, "Ricerca linea...")
                routes_search = input_msg.replace('/','')
                routes_search = str(routes_search)
                r = requests.get("http://127.0.0.1:9543/{0}".format(routes_search))
                self.myresult = r.json()
                if(self.myresult['result'] != []):
                    bot.sendMessage(chat_id, "Mandami la tua posizione per la fermata più vicina!")
                    self.USER_STATE[chat_id] = 3
                else:
                    bot.sendMessage(chat_id, "Linea non valida...Riprova o torna alla /HOME!")
            elif input_msg == "Fermata" and \
                self.USER_STATE[chat_id] == 1:
                entries = [["Pesaro", "Fano"],["Urbino", "Di Quartiere"],["SCOLASTICA"],["HOME"]]
                markup = ReplyKeyboardMarkup(keyboard=entries)
                bot.sendMessage(chat_id,'Scegli l\'opzione',reply_markup=markup)
                self.USER_STATE[chat_id] = 1.22

            elif self.USER_STATE[chat_id] == 1.22:
                r = requests.get("http://127.0.0.1:9543/fermate/{0}".format(input_msg))
                self.myresult = r.json()
                i = 0
                self.count2 = i
                self.count = 10
                print(len(self.myresult))
                try:
                    self.myresult = self.myresult['result']

                    for x in self.myresult:

                        if self.count2 <= self.count:
                            bot.sendMessage(chat_id, "/"+self.myresult[self.count2][0]+" "+self.myresult[self.count2][1])
                            self.count2 = i

                        elif i == (len(self.myresult) - 1):
                            bot.sendMessage(chat_id, "/other o /HOME", reply_markup=ReplyKeyboardRemove())
                            self.count = self.count + 10
                            self.USER_STATE[chat_id] = 5

                        i = i+1
                except(KeyError):
                    bot.sendMessage(chat_id, 'Errore, fermate non trovate')

            elif input_msg == "/other" and self.USER_STATE[chat_id] == 5:
                i = 0

                for x in self.myresult:

                    if self.count2 <= self.count and self.count < len(self.myresult):
                        bot.sendMessage(chat_id, "/"+self.myresult[self.count2][0]+" "+self.myresult[self.count2][1])
                        self.count2 = self.count2 + 1

                    elif i == (len(self.myresult) - 1) and self.count < len(self.myresult):
                        bot.sendMessage(chat_id, "/other o /HOME")
                        self.count = self.count + 10

                    elif self.count >= len(self.myresult) and i == (len(self.myresult) - 1):
                        bot.sendMessage(chat_id, "Linee terminate /HOME")

                    i = i+1
                    self.USER_STATE[chat_id] = 5

            elif input_msg == "Prezzi" and \
                self.USER_STATE[chat_id] == 1:
                    entries = [["ExtraUrbane", "Urbane"],["HOME"]]
                    markup = ReplyKeyboardMarkup(keyboard=entries)
                    bot.sendMessage(chat_id,'Scegli l\'opzione',reply_markup=markup)
                    self.USER_STATE[chat_id] = 1.3



            elif self.USER_STATE[chat_id] == 1.3:

                self.lista_costi = []
                if input_msg == "ExtraUrbane":

                    try:
                        sauce = urllib.request.urlopen(URL_EXTRAURBANE).read()
                        soup = bs.BeautifulSoup(sauce, 'html.parser')
                        i= 0
                        j = 0

                        for item in soup.find_all('p'):

                            if j != 0 and j != -5:
                                answer = ''.join(item.text)

                                if j < 5 and j != 0:
                                    self.lista_descrizione.append(answer)
                                    j = j+1

                                elif answer == '3,70':
                                    j = -5
                                    self.lista_costi.append(answer)

                                else:
                                    self.lista_costi.append(answer)

                            elif i == 5 and j == 0:
                                i = -1
                                j = j+1

                            i = i+1

                    except urllib.error.HTTPError as err:

                        if err.code == 404:
                            bot.sendMessage(chat_id, 'ERRORE')
                    i = 0
                    testo = ''

                    for dato in self.lista_costi:

                        if i < 3:
                            testo = testo+dato+ " | "

                        elif i < 7 and i >= 3:
                            print(dato)

                        else:
                            testo = testo+"\n-----------------------\n"+dato+ " | "
                            i = 0

                        i = i+1
                    bot.sendMessage(chat_id, testo)


                elif input_msg == "Urbane":
                    try:
                        k = 0
                        testo = ''
                        sauce = urllib.request.urlopen(URL_URBANE).read()
                        soup = bs.BeautifulSoup(sauce, 'html.parser')
                        for item in soup.find_all('td'):
                            answer = ''.join(item.text)
                            if k != 1:
                                self.lista_costi.append(answer)

                                if(item.text == '11,20'):
                                    k = 1

                    except urllib.error.HTTPError as err:
                        if err.code == 404:
                            bot.sendMessage(chat_id, 'ERRORE')
                    for dato in self.lista_costi:
                        testo = testo+dato+ " | "
                    bot.sendMessage(chat_id, testo)
                else:
                    bot.sendMessage(chat_id, 'Opzione non valida, riprova')
            else:
                bot.sendMessage(chat_id, 'Opzione non valida')
                self.send_options(chat_id)





        elif content_type == 'location' and \
                self.USER_STATE[chat_id] == 3:
                latitude = float(msg["location"]["latitude"])
                longitude = float(msg["location"]["longitude"])
                i = 0

                for x in self.myresult['result']:
                    app_stop = str(x[0])
                    r = requests.get("http://127.0.0.1:9543/fermata/{0}".format(app_stop))
                    newresult = r.json()
                    newresult = newresult['result']
                    latitude_2 = float(newresult[0][0])
                    longitude_2 = float(newresult[0][1])

                    if i == 0:
                        min = math.sqrt((latitude_2-latitude)**2 + (longitude_2-longitude)**2)
                        fermata_giusta = newresult
                        i = i+1

                    else:
                        temp = math.sqrt((latitude_2-latitude)**2 + (longitude_2-longitude)**2)

                        if temp < min:
                            min = temp
                            fermata_giusta = newresult

                origins = str(latitude)+","+str(longitude)
                latitudine = str(float(fermata_giusta[0][0]))
                longitudine = str(float(fermata_giusta[0][1]))
                destinations = latitudine+","+longitudine
                mode = 'walking'
                URL = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+latitudine+","+longitudine+"&key="+API_KEY
                r = requests.get(url = URL)
                data = r.json()
                via = data['results'][0]['address_components'][1]['short_name']
                URL = str("https://maps.googleapis.com/maps/api/distancematrix/json?origins="+str(origins)+"&destinations="+str(destinations)+"&mode="+mode+"&key="+API_KEY)
                r = requests.get(url = URL)
                data = r.json()

                distance = data["rows"][0]["elements"][0]["distance"]["text"]
                duration = data["rows"][0]["elements"][0]["duration"]["text"]
                bot.sendLocation(chat_id, float(fermata_giusta[0][0]),float(fermata_giusta[0][1]))
                bot.sendMessage(chat_id, via+" dista: "+distance+" tempo a piedi: "+duration+"\n /HOME")

        else:
            bot.sendMessage(chat_id, 'NON RICONOSCO IL CARATTERE')


        cnx.close()

    def send_options(self, chat_id):
        entries = [["Linea", "Fermata", "Prezzi"]]
        markup = ReplyKeyboardMarkup(keyboard=entries)
        bot.sendMessage(chat_id,'Scegli un opzione', reply_markup=markup)
        self.USER_STATE[chat_id] = 1



cnx = mysql.connector.connect(user='root', password='doremi666', host='localhost', database='mydb')
mycursor = cnx.cursor()
handler = MessageHandler()
bot = telepot.Bot(TOKEN)
bot.message_loop({'chat':handler.handle})

while 1:
    time.sleep(10)
