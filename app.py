from flask import Flask, jsonify, request
import traceback
from test_mongo_data import Mdb
from test.data_generator.data_generator import Arrangement

from config import ITEM, CONTAINER, ARRANGEMENT, SNAPSHOT
import json
from bson import ObjectId
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
mdb = Mdb()
arrangement_obj = Arrangement()

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@app.route("/")
def home_page():
    return "Arrange That!"


@app.route('/arrangement', methods=['POST'])
@app.route('/api/v1/arrangement', methods=['POST'])
def save_arrangement():
    arrangement = request.json
    json_data = validate_arrangement(arrangement)
    if json_data == True:
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


@app.route('/arrangement', methods=['GET'])
@app.route('/api/v1/arrangement', methods=['GET'])
@app.route('/arrangement/<string:arrangement_id>', methods=['GET'])
@app.route('/api/v1/arrangement/<string:arrangement_id>', methods=['GET'])
def get_arrangement(arrangement_id=None):
    if arrangement_id is None:
        return JSONEncoder().encode(mdb.get_all_arrangements())
    else:
        return mdb.get_arrangement_by_id(arrangement_id)


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
            if snapshot_id == "" or snapshot_name == "" or snapshot_dict == "":
                return False
            else:
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
