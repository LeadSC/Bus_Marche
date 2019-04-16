import telepot
import csv
import math
from config import TOKEN, API_KEY
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

lista_costi = []
lista_descrizione = []
dati1 =[()]
dati2 =[()]
dati3 =[()]
dati4 =[]
count = 0
count2 = 0
user_state = 0
myresult = []
cake = emojize(":cake:", use_aliases=True)


def handle(msg):

    global lista_descrizione
    global lista_costi
    global dati1
    global dati2
    global dati3
    global user_state
    global myresult
    global count
    global count2
    global dati4

    cnx = mysql.connector.connect(user='root', password='doremi666', host='localhost', database='mydb')
    mycursor = cnx.cursor()

    content_type, chat_type, chat_id = telepot.glance(msg)

    keyboardd = InlineKeyboardMarkup(inline_keyboard=[
                     [InlineKeyboardButton(text='Yes', callback_data='yes'),
                     InlineKeyboardButton(text='No', callback_data='no')],
                 ])


    if content_type == "text":
        msgg = json.dumps(msg, indent=4)
        input_msg = msg['text']
        print(msgg)

        if input_msg == "/inizia" and \
            user_state == 0:
            entries = [["Linea", "Fermata", "Prezzi"]]
            markup = ReplyKeyboardMarkup(keyboard=entries)
            bot.sendMessage(chat_id,'Scegli l\'opzione',reply_markup=markup)
            user_state = 1

        elif input_msg == "/start" and \
            user_state == 0:
            bot.sendMessage(chat_id, "Benvenuto "+msg['chat']['first_name']+" questo bot è inutile al cazzo l\'abbiamo fatto solo per un esame del cazzo e questo è il risultato, non criticare grazie! o se proprio hai da criticare critica @wepesarobot")

        elif msg['text'] == "Linea" and \
            user_state == 1:
            bot.sendMessage(chat_id, 'Digita la linea che vuoi cercare...')
            user_state = 2

        elif (user_state == 2 or user_state == 5) and msg['text'] != "/other":
            bot.sendMessage(chat_id, "Ricerca linea...")
            routes_search = msg['text'].replace('/','')
            routes_search = str(routes_search)
            r = requests.get("http://127.0.0.1:9543/{0}".format(routes_search))
            myresult = r.json()
            print(myresult['result'])
            bot.sendMessage(chat_id, "Mandami la tua posizione per la fermata più vicina!")
            user_state = 3

        elif msg['text'] == "Fermata" and \
            user_state == 1:
            entries = [["Pesaro", "Fano"],["Urbino", "Di Quartiere"],["SCOLASTICA"]]
            markup = ReplyKeyboardMarkup(keyboard=entries)
            bot.sendMessage(chat_id,'Scegli l\'opzione',reply_markup=markup)
            user_state = 1.22

        elif user_state == 1.22:
            r = requests.get("http://127.0.0.1:9543/fermate/{0}".format(msg['text']))
            myresult = r.json()
            i = 0
            count = 10
            print(len(myresult))
            myresult = myresult['result']

            for x in myresult:

                if count2 <= count:
                    bot.sendMessage(chat_id, "/"+myresult[count2][0]+" "+myresult[count2][1])
                    count2 = i

                elif i == (len(myresult) - 1):
                    bot.sendMessage(chat_id, "/other")
                    count = count + 10
                    user_state = 5

                i = i+1

        elif msg['text'] == "/other":
            i = 0

            for x in myresult:

                if count2 <= count and count < len(myresult):
                    bot.sendMessage(chat_id, "/"+myresult[count2][0])
                    count2 = count2 + 1

                elif i == (len(myresult) - 1) and count < len(myresult):
                    bot.sendMessage(chat_id, "/other")
                    count = count + 10

                elif count >= len(myresult) and i == (len(myresult) - 1):
                    bot.sendMessage(chat_id, "Linee terminate")

                i = i+1
                user_state = 5

        elif msg['text'] == "Prezzi" and \
            user_state == 1:
                entries = [["ExtraUrbane", "Urbane"]]
                markup = ReplyKeyboardMarkup(keyboard=entries)
                bot.sendMessage(chat_id,'Scegli l\'opzione',reply_markup=markup)
                user_state = 1.2

        elif user_state == 1.2 and msg['text'] == "Urbane":
            entries = [["Pesaro", "Fano"],["Urbino"]]
            markup = ReplyKeyboardMarkup(keyboard=entries)
            bot.sendMessage(chat_id,'Scegli l\'opzione',reply_markup=markup)

        elif user_state == 1.3 or msg['text'] == "ExtraUrbane":

            if msg['text'] == "ExtraUrbane":
                URL = "http://www.adriabus.eu/viewdoc.asp?co_id=7703"

                try:
                    sauce = urllib.request.urlopen(URL).read()
                    soup = bs.BeautifulSoup(sauce, 'html.parser')
                    i= 0
                    j = 0

                    for item in soup.find_all('p'):

                        if j != 0 and j != -5:
                            answer = ''.join(item.text)

                            if j < 5 and j != 0:
                                lista_descrizione.append(answer)
                                j = j+1

                            elif answer == '3,70':
                                j = -5
                                lista_costi.append(answer)

                            else:
                                lista_costi.append(answer)

                        elif i == 5 and j == 0:
                            i = -1
                            j = j+1

                        i = i+1

                except urllib.error.HTTPError as err:

                    if err.code == 404:
                        bot.sendMessage(chat_id, msg)
                i = 0
                testo = ''

                for dato in lista_costi:

                    if i < 3:
                        testo = testo+dato+ " | "

                    elif i < 7 and i >= 3:
                        print(dato)

                    else:
                        testo = testo+"\n-----------------------\n"+dato+ " | "
                        i = 0

                    i = i+1
                    print(dato)

                bot.sendMessage(chat_id, testo)
                bot.sendMessage(chat_id, "Vuoi scoprire la distanza della tua tratta?", reply_markup=keyboardd)

    elif content_type == 'location' and \
            user_state == 3:
            latitude = float(msg["location"]["latitude"])
            longitude = float(msg["location"]["longitude"])
            i = 0

            for x in myresult['result']:
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
            destinations = str(float(fermata_giusta[0][0]))+","+str(float(fermata_giusta[0][1]))
            mode = 'walking'
            URL = str("https://maps.googleapis.com/maps/api/distancematrix/json?origins="+str(origins)+"&destinations="+str(destinations)+"&mode="+mode+"&key="+API_KEY)
            r = requests.get(url = URL)
            data = r.json()
            print(data["rows"])
            distance = data["rows"][0]["elements"][0]["distance"]["text"]
            duration = data["rows"][0]["elements"][0]["duration"]["text"]
            bot.sendLocation(chat_id, float(fermata_giusta[0][0]),float(fermata_giusta[0][1]))
            bot.sendMessage(chat_id, str(fermata_giusta)+" dista: "+distance+" tempo a piedi: "+duration)
            user_state = 0

    cnx.close()

def send_options(self, chat_id):
    entries = [["Linea", "Fermata", "Via"]]
    markup = ReplyKeyboardMarkup(keyboard=entries)
    bot.sendMessage(chat_id, reply_markup=markup)

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print("Callback Query: ", query_id, from_id, query_data)
    bot.answerCallbackQuery(query_id, text="YEAH")

bot = telepot.Bot(TOKEN)
bot.message_loop({'chat':handle,
                  'callback_query': on_callback_query})

while 1:
    time.sleep(10)
