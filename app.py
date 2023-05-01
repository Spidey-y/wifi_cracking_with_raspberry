from time import sleep
from flask import Flask, jsonify, render_template
from flask_restful import Resource, Api, reqparse
from functions.get_wifi_name import getWifiList
from flask_swagger_ui import get_swaggerui_blueprint
import json
from functions.handshake import get_handshake
from functions.crack_wifi import crack_wifi
from functions.database import check_database, create_connection


app = Flask(__name__)
api = Api(app)


@app.route('/')
def index():
    wifi_list = getWifiList()
    return render_template('index.html', ssids=wifi_list)


class CrackWifi(Resource):
    def get(self):
        wifi_list = getWifiList()
        parser = reqparse.RequestParser()
        parser.add_argument('ssid', type=str, location='args')
        args = parser.parse_args()
        if args['ssid'] not in wifi_list:
            return jsonify({'error': 'ssid not found'})
        sleep(3)
        #TODO: Crack wifi password
        # conn = check_database()
        # cur = conn.cursor()
        # crack_wifi(args['ssid'])
        # cur.execute("INSERT INTO saved_passwords (ssid, password) VALUES (?, ?)", ('my_ssid', 'my_password'))
        # conn.commit()
        # conn.close()
        return jsonify({'ssid': args['ssid']})


class GetHandshake(Resource):
    def get(self):
        wifi_list = getWifiList()
        parser = reqparse.RequestParser()
        parser.add_argument('ssid', type=str, location='args')
        args = parser.parse_args()
        if args['ssid'] not in wifi_list:
            return jsonify({'error': 'ssid not found'})
        #TODO: implement handshake function (in functions/handshake.py)
        sleep(3)
        # get_handshake(args['ssid'])
        # conn = check_database()
        # cur = conn.cursor()
        # cur.execute("INSERT INTO saved_handshakes (ssid, handshake) VALUES (?, ?)", ('my_ssid', handshake_data))
        # conn.commit()
        # conn.close()
        return jsonify({'handshake': 'handshake file'})


# saved passwords and handshakes
class SavedPasswords(Resource):
    def get(self):
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM saved_passwords")
        rows = cur.fetchall()
        conn.close()
        return jsonify(rows)
    
   
class SavedHandshakes(Resource):
    def get(self):
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM saved_handshakes")
        rows = cur.fetchall()
        conn.close()
        print(rows)
        return jsonify(rows)


api.add_resource(CrackWifi, '/crack_wifi')
api.add_resource(GetHandshake, '/handshake')
api.add_resource(SavedPasswords, '/saved_passwords')
api.add_resource(SavedHandshakes, '/saved_handshakes')


check_database()
# conn = create_connection()
# cur = conn.cursor()
# cur.execute("SELECT * FROM saved_handshakes")
# rows = cur.fetchall()
# cur.execute("INSERT INTO saved_handshakes (ssid, handshake) VALUES (?, ?)", ('my_ssid3', 'aadada'))
# cur.execute("INSERT INTO saved_handshakes (ssid, handshake) VALUES (?, ?)", ('my_ssid2', 'abcd'))
# cur.execute("INSERT INTO saved_handshakes (ssid, handshake) VALUES (?, ?)", ('my_ssid1', 'aaaa'))
# conn.commit()
# conn.close()

if __name__ == '__main__':
    app.run(debug=True)