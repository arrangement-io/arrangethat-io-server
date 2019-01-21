from flask import Flask, jsonify, request, session, redirect, url_for
from flask_cors import CORS
from flask_oauth import OAuth
from bson import ObjectId
import json
import os
import traceback
from config import ITEM, CONTAINER, ARRANGEMENT, SNAPSHOT, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, REDIRECT_URI
from test_mongo_data import Mdb
from test.data_generator.data_generator import Arrangement

SECRET_KEY = 'development key'
DEBUG = True

app = Flask(__name__)
oauth = OAuth()
CORS(app)
mdb = Mdb()
export = Export()
arrangement_obj = Arrangement()
app.debug = DEBUG
app.secret_key = SECRET_KEY

google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@app.route("/")
def home_page():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login'))

    access_token = access_token[0]
    from urllib2 import Request, urlopen, URLError

    headers = {'Authorization': 'OAuth '+access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
    try:
        res = urlopen(req)
    except URLError, e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('login'))
        return res.read()

    return res.read()

def get_current_user():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login'))

    access_token = access_token[0]
    from urllib2 import Request, urlopen, URLError

    headers = {'Authorization': 'OAuth ' + access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
    try:
        res = urlopen(req)
    except URLError, e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('login'))
        return res.read()

    google_res = res.read()
    if google_res:
        return google_res['id']

    return None

@app.route("/login", methods=['POST'])
def login():
    data = request.json
    session['access_token'] = data['access_token'], ''
    return jsonify({'message':'You are logged in.'})

# @app.route("/login")
# def login():
#     callback=url_for('authorized', _external=True)
#     return google.authorize(callback=callback)

@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('home_page'))

@google.tokengetter
def get_access_token():
    return session.get('access_token')

@app.route('/arrangement', methods=['POST'])
@app.route('/api/v1/arrangement', methods=['POST'])
def save_arrangement():
    arrangement = request.json
    json_data = validate_arrangement(arrangement)

    if json_data:
        arrangement_obj.pass_json(arrangement)
        data = arrangement_obj.build()
        arrangement_exists = mdb.check_arrangement_exists(data)
        if arrangement_exists:
            mdb.replace_arrangement(data)
        else:
            mdb.add_arrangement(data)
        return JSONEncoder().encode(data)
    else:
        return jsonify({'message':'json is not validate'})


@app.route('/arrangements/<string:user_id>', methods=['GET'])
@app.route('/api/v1/arrangements/<string:user_id>', methods=['GET'])
def get_arrangements(user_id):
    if user_id is None:
        return None
    result = mdb.get_all_arrangements_by_user(user_id)
    return jsonify({"arrangements": result})


@app.route('/arrangement', methods=['GET'])
@app.route('/api/v1/arrangement', methods=['GET'])
@app.route('/arrangement/<string:arrangement_id>/<string:export_type>', methods=['GET'])
@app.route('/api/v1/arrangement/<string:arrangement_id>', methods=['GET'])
def get_arrangement(arrangement_id=None, export_type=None):
    current_user = get_current_user()

    if arrangement_id is None:
        arrangements = mdb.get_all_arrangements_by_user(current_user)
        arrangement_list = []
        for arr in arrangements:
            arrangement_list.append({"id": arr['_id'], "title": arr['name']})

        return JSONEncoder().encode(arrangement_list)
    else:
        arrangements = mdb.get_arrangement_by_id(arrangement_id)
        return export.get_arrangements(export_type, arrangements)


def validate_arrangement(arrangement):
    try:
        arrangement_id = arrangement['_id']
        name = arrangement['name']
        timestamp = arrangement['timestamp']
        modified_timestamp = arrangement['modified_timestamp']
        is_deleted = arrangement['is_deleted']
        items = arrangement['items']
        item_id_list = []
        for item in items:
            item_id = item['_id']
            item_name = item['name']
            item_size = item['size']
            item_id_list.append(item_id)
            if item_id == "" or item_name == "" or item_size == "":
                return False
        containers = arrangement['containers']
        container_id_list = []
        for container in containers:
            container_id = container['_id']
            container_name = container['name']
            container_size = container['size']
            container_id_list.append(container_id)
            if container_id == "" or container_name == "" or container_size == "":
                return False
        snapshots = arrangement['snapshots']
        for snapshot in snapshots:
            snapshot_id = snapshot['_id']
            snapshot_name = snapshot['name']
            snapshot_dict = snapshot['snapshot']
            snapshot_list = snapshot['unassigned']
            if snapshot_id == "" or snapshot_name == "" or snapshot_dict == "" or snapshot_list == "":
                return False
            else:
                if snapshot_list == []:
                    pass
                else:
                    for data in snapshot_list:
                        if data in item_id_list:
                            print(data)
                        else:
                            return False
                for key, value in snapshot_dict.items():
                    container_key_id = key
                    if container_key_id in container_id_list:
                        for item_value_id in value:
                            if item_value_id in item_id_list:
                                if container_key_id == "" or not item_value_id:
                                    return False
                            else:
                                return False
                    else:
                        return False

        if(arrangement_id and name and timestamp and modified_timestamp and item_id
                and item_name and item_size and container_id and container_name
                and container_size and snapshot_id and snapshot_name and container_key_id
                and item_value_id and not is_deleted):
            return True
        else:
            return False
    except Exception as exe:
        print("validate_arrangement() :: Got exception: %s: ", exe)
        print(traceback.format_exc())
        return False

if __name__ == '__main__':
    app.run(host = 'localhost', port = 8080, debug = True)
