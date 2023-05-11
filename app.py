from time import sleep
from flask import Flask, jsonify, render_template, send_from_directory
from flask_restful import Resource, Api, reqparse
from functions.get_wifi_name import getWifiList
from flask_swagger_ui import get_swaggerui_blueprint
import json
from functions.handshake import get_handshake
from functions.crack_wifi import crack_wifi
from functions.database import check_database, create_connection
import os
app = Flask(__name__)
api = Api(app)


@app.route('/')
def index():
    wifi_list = getWifiList()
    return render_template('index.html', ssids=wifi_list)


class CrackWifi(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ssid', type=str, location='args')
        parser.add_argument('bss', type=str, location='args')
        args = parser.parse_args()
        ssid = args['ssid'].replace(" ", "_")
        if not os.path.isfile(f"./{ssid}_{args['bss']}.cap"):
            return jsonify({'error': 'handshake not found'})
        password = crack_wifi(args['ssid'], args['bss'])   
        if "KEY FOUND!" in password:
            pw = password[13:]
            pw = pw[:-2]
            conn = check_database()
            cur = conn.cursor()
            cur.execute("INSERT INTO saved_passwords (ssid, password) VALUES (?, ?)", (args['ssid'], pw))
            conn.commit()
            conn.close()
            return jsonify({'password': pw})
        else:
            return jsonify({'password': 'password not found'})


class GetHandshake(Resource):
    def get(self):
        wifi_list = getWifiList()
        parser = reqparse.RequestParser()
        parser.add_argument('ssid', type=str, location='args')
        parser.add_argument('bss', type=str, location='args')
        parser.add_argument('channel', type=str, location='args')
        args = parser.parse_args()
        ssid = args['ssid'].replace(" ", "_")
        if args['bss'] not in list(wifi_list.keys()):
            return jsonify({'error': 'ssid not found'})
        if os.path.isfile(f"./{ssid}_{args['bss']}.cap"):
            path = f"{ssid}_{args['bss']}.cap"
        else:
            path = get_handshake(args['ssid'], args['bss'], args['channel'])
            conn = check_database()
            cur = conn.cursor()
            cur.execute("INSERT INTO saved_handshakes (ssid, handshake) VALUES (?, ?)", (args['ssid'], path))
            conn.commit()
            conn.close()  
        return jsonify({'handshake': 'Download handshake', 'link': path})

@app.route('/handshakes/<path:filename>')
def download_file(filename):
    return send_from_directory("", filename, as_attachment=True)
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