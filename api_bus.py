import mysql.connector
import json
import csv
import urllib.request

from flask import Flask, request
from flask_restful import Resource, Api

#Init flask
app = Flask(__name__)
api = Api(app)
PORT = 9543


class Query_Fermate_Linea(Resource):

    def get(self, routes_search):


        mycursor.execute("SELECT DISTINCT stop_times.stop_id from routes, trips, stop_times where routes.agency_id = 'ADRIABUS' and routes.route_short_name = \'"+str(routes_search)+"\' and  trips.route_id = routes.route_id and stop_times.trip_id = trips.trip_id")

        myresult = mycursor.fetchall()

        rv = []

        for result in myresult:
            rv.append(result)


        return {"status": 200, "result": rv}, 200

class Query_Tipo_Linee(Resource):

    def get(self, localita):

        print(localita)

        if localita == "Pesaro":
            mycursor.execute("SELECT DISTINCT routes.route_short_name, routes.route_long_name from routes where routes.agency_id = 'ADRIABUS' and (routes.route_short_name LIKE 'P%' or routes.route_long_name like '%PESARO%')")
        elif localita == "Fano":
            mycursor.execute("SELECT DISTINCT routes.route_short_name, routes.route_long_name from routes where routes.agency_id = 'ADRIABUS' and routes.route_short_name LIKE 'F%' or routes.route_long_name like '%FANO%'")
        elif localita == "Urbino":
            mycursor.execute("SELECT distinct routes.route_short_name, routes.route_long_name from routes where routes.agency_id = 'ADRIABUS' and routes.route_short_name LIKE 'U%' or routes.route_long_name like '%URBINO%'")
        elif localita == "Di Quartiere":
            mycursor.execute("SELECT distinct routes.route_short_name, routes.route_long_name from routes where routes.agency_id = 'ADRIABUS' and routes.route_short_name NOT LIKE 'F%' and routes.route_short_name NOT LIKE 'U%' and routes.route_short_name NOT LIKE 'P%'")
        elif localita == "SCOLASTICA":
            mycursor.execute("SELECT distinct routes.route_short_name, routes.route_long_name from routes where routes.agency_id = 'ADRIABUS' and routes.route_long_name like '%SCOLASTICA%'")

        myresult = mycursor.fetchall()

        rv = []

        for result in myresult:
            rv.append(result)


        return {"status": 200, "result": rv}, 200

class Query_Fermata_Prossima(Resource):

    def get(self, app_stop):

        mycursor.execute("SELECT stops.stop_lat, stops.stop_lon from stops where stops.stop_id = \'"+app_stop+"\'")

        myresult = mycursor.fetchall()

        rv = []

        for result in myresult:
            rv.append(result)


        return {"status": 200, "result": rv}, 200





api.add_resource(Query_Fermate_Linea, '/<routes_search>')
api.add_resource(Query_Tipo_Linee, '/fermate/<localita>')
api.add_resource(Query_Fermata_Prossima, '/fermata/<app_stop>')
#api.add_resource(ApiGoogle, '/signup/')

if __name__ == '__main__':
    try:
        cnx = mysql.connector.connect(user='root', password='doremi666', host='localhost', database='mydb')
        mycursor = cnx.cursor()
        app.run(host='127.0.0.1', port=PORT)

    finally:
        cnx.close()
