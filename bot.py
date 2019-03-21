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

dati1 =[()]
dati2 =[()]
dati3 =[()]
dati4 =[]
user_state = 0
def handle(msg):
#########################################
#elif input_msg == "Classico" and \
#                    (self.USER_STATE[chat_id] == 1 or self.USER_STATE[chat_id] == 2):
#       self.USER_STATE[chat_id] = (self.USER_STATE[chat_id] * 10) + 2
#########################################
    global dati1
    global dati2
    global dati3
    global user_state
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == "text":
        msgg = json.dumps(msg, indent=4)
        input_msg = msg['text']
        print(msgg)
        if input_msg == "/inizia" and \
            user_state == 0:
            entries = [["Linea", "Fermata", "Via"]]
            markup = ReplyKeyboardMarkup(keyboard=entries)
            bot.sendMessage(chat_id,'Scegli l''opzione',reply_markup=markup)
            user_state = 1
        elif msg['text'] == "Linea" and \
            user_state == 1:
            bot.sendMessage(chat_id, 'Digita la linea che vuoi cercare...')
            user_state = 2
        elif user_state == 2:
            routes_search = msg['text']
            with open("./routes.txt", newline="") as filecsv:
                lettore = csv.reader(filecsv,delimiter=",")
                #filtro dati adriabus che
                dati = [(riga[0]) for riga in lettore if riga[1] == "ADRIABUS" and riga[2] == routes_search]
                #print(dati)
                route_id = dati[0]
                #print(route_id)
                #filtra file trips.txt ricavi trip_id
            with open("./trips.txt", newline="") as filecsv:
                lettore = csv.reader(filecsv,delimiter=",")
                dati1 = [(riga[1]) for riga in lettore if riga[0] == route_id]
                print(dati1)

        #stoptimes.txt stop_id
            with open("./stop_times.txt", newline="") as filecsv:
                lettore = csv.reader(filecsv,delimiter=",")
                dati2 = [(riga[0],riga[1],riga[2],riga[3]) for riga in lettore if (riga[0] in dati1)]
                print(dati2)
                dati22 =[(value[3])for value in dati2]

        #stop_id stops.txt prendo latitudine e longitudine
            with open("./stops.txt", newline="") as filecsv:
                lettore = csv.reader(filecsv,delimiter=",")
                dati3 = [(riga[2],riga[3],riga[1],riga[0]) for riga in lettore if (riga[0] in dati22)]
                print(dati3)
        #richiedi posizione e verifica quella più vicino di lista 3
        #bot.sendMessage(chat_id, "Mandami la tua posizione per la fermata più vicina!")
        #if()

            bot.sendMessage(chat_id, "Mandami la tua posizione per la fermata più vicina!")
            user_state = 3
    elif content_type == 'location':
        if user_state == 3:
            latitude = float(msg["location"]["latitude"])
            longitude = float(msg["location"]["longitude"])
            i = 0
            for dato in dati3:
                latitude_2 = float(dato[0])
                longitude_2 = float(dato[1])
                if i == 0:
                    min = math.sqrt((latitude_2-latitude)**2 + (longitude_2-longitude)**2)
                    fermata_giusta = dato
                    i = i+1
                else:
                    temp = math.sqrt((latitude_2-latitude)**2 + (longitude_2-longitude)**2)
                    if temp < min:
                        min = temp
                        fermata_giusta = dato




            origins = str(latitude)+","+str(longitude)
            destinations = str(float(fermata_giusta[0]))+","+str(float(fermata_giusta[1]))
            mode = 'walking'

            URL = str("https://maps.googleapis.com/maps/api/distancematrix/json?origins="+str(origins)+"&destinations="+str(destinations)+"&mode="+mode+"&key="+API_KEY)
            r = requests.get(url = URL)
            data = r.json()
            #data = json.dumps(data, indent=4)
            #data = json.dumps(r.json(), indent=2, sort_keys=True)

            print(data["rows"])
            distance = data["rows"][0]["elements"][0]["distance"]["text"]
            duration = data["rows"][0]["elements"][0]["duration"]["text"]
            #filehandle = urllib.request.urlopen(URL)
            global dati4
            for dato in dati2:
                for dato1 in dati1:
                    if(dato1 in dato[0] and fermata_giusta[3] in dato[3]):
                        dati4.append(dato[1])

            print(dati4)

            # i = 0
            # for dato in dati1:
            #     if(dati1[i] in dati2 and feramata_giusta[3] in dati2):
            #         dati4.append(dato)
            #     if(i+1 < len(dati1)):
            #         i = i+1
            #
            # print (dati4)
            #destinations: San+Francisco|Victoria+BC
            bot.sendLocation(chat_id, float(fermata_giusta[0]),float(fermata_giusta[1]))
            bot.sendMessage(chat_id, str(fermata_giusta)+" dista: "+distance+" tempo a piedi: "+duration)
            #print(distance)
            bot.sendMessage(chat_id, str(dati4))
            user_state = 0
            #mode: driving
            #key: API_KEY
    else:
        entries = [["Pranzo"], ["Cena"]]
        markup = ReplyKeyboardMarkup(keyboard=entries)
        bot.sendMessage(chat_id, 'Use inline keyboard', reply_markup=markup)
    #entries = [["Classico"], ["Cibus"]]
#markup = ReplyKeyboardMarkup(keyboard=entries)
    #ry:from math import sqrt
    #    sauce = urllib.request.urlopen("http://www.trasporti.marche.it/downloads/opendata/richiesta/default.htm").read()
    #    soup = bs.BeautifulSoup(sauce, 'html.parser')
        # cercare i tag span con classe abuot stat
    #    for item in soup.find_all('a'):
    #        print(item)
    #        bot.sendMessage(chat_id, item.text)
    #except urllib.error.HTTPError as err:
    #    if err.code == 404:
    #        bot.sendMessage(chat_id, msg)

        #cercare cosa prelevare
    # inviando la mia posizione ricavo latitudine e longitudine

    if content_type == 'location':
        latitude = msg["location"]["latitude"]
        longitude = msg["location"]["longitude"]
    #else:
        #bot.sendMessage(chat_id, "Errore, posizione non valida!")
    #name = msg["from"]["first_name"]
    #txt = msg['text']
    #bot.sendMessage(chat_id, "schiaccia",reply_markup=keyboard)
        #bot.sendMessage(chat_id,reply_markup=keyboard)

def send_options(self, chat_id):
    entries = [["Linea", "Fermata", "Via"]]
    markup = ReplyKeyboardMarkup(keyboard=entries)
    bot.sendMessage(chat_id, reply_markup=markup)

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print("Callback Query: ", query_id, from_id, query_data)
    bot.answerCallbackQuery(query_id, text="YEAH")



#bot = telepot.Bot(TOKEN)
#response = bot.getUpdates()


#pprint(response)
#bot.message_loop({'chat': on_chat_message,
#                  'callback_query': on_callback_query})

#eyboard = InlineKeyboardMarkup(inline_keyboard=[
#                     [InlineKeyboardButton(text='IP', callback_data='ip'),
#                     InlineKeyboardButton(text='Info', callback_data='info'),
#                     InlineKeyboardButton(text='Time', callback_data='time')],
#                 ])
bot = telepot.Bot(TOKEN)
bot.message_loop({'chat':handle,
                  'callback_query': on_callback_query})

#print ('Listening ...')
while 1:
    time.sleep(10)
