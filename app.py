from flask import Flask, jsonify, request
import traceback
import random
import datetime
from test_mongo_data import Mdb
from config import ITEM, CONTAINER, ARRANGEMENT, SNAPSHOT
import json
from bson import ObjectId

app = Flask(__name__)
mdb = Mdb()

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def uniqueid():
    seed = random.getrandbits(32)
    while True:
        yield seed
        seed += 1


@app.route("/")
def home_page():
    return "Arrange That!"


@app.route('/arrangements', methods=['POST'])
@app.route('/api/v1/arrangements', methods=['POST'])
def save_arrangement():
    arrangement = request.json
    json_data = validate_arrangement(arrangement)
    if json_data == True:
        arrangement_exists = mdb.check_arrangement_exists(arrangement)
        if arrangement_exists:
            mdb.replace_arrangement(arrangement)
        else:
            mdb.add_arrangement(arrangement)
        return JSONEncoder().encode(arrangement)
    else:
        return jsonify({'message':'json is not validate'})


@app.route('/arrangements', methods=['GET'])
@app.route('/api/v1/arrangements', methods=['GET'])
@app.route('/arrangements/<string:arrangement_id>', methods=['GET'])
@app.route('/api/v1/arrangements/<string:arrangement_id>', methods=['GET'])
def get_arrangement(arrangement_id=None):
    if arrangement_id is None:
        return JSONEncoder().encode(mdb.get_all_arrangements())
    else:
        return mdb.get_arrangement_by_id(arrangement_id)


def validate_arrangement(arrangement):
    try:
        item_id = ''
        item_name = ''
        item_size = ''
        container_id = ''
        container_name = ''
        container_size = ''
        snapshot_id = ''
        snapshot_name = ''
        container_key_id = ''
        item_value_id = ''

        arrangement_id = arrangement['id']
        name = arrangement['name']
        timestamp = arrangement['timestamp']
        is_deleted = arrangement['is_deleted']
        items = arrangement['items']

        for item in items:
            item_id = item['id']
            item_name = item['name']
            item_size = item['size']
            if item_id == "" or item_name == "" or item_size == "":
                break

        containers = arrangement['containers']
        for container in containers:
            container_id = container['id']
            container_name = container['name']
            container_size = container['size']
            if container_id == "" or container_name == "" or container_size == "":
                break

        snapshots = arrangement['snapshots']
        for snapshot in snapshots:
            snapshot_id = snapshot['id']
            snapshot_name = snapshot['name']
            snapshot_dict = snapshot['snapshot']
            if snapshot_id == "" or snapshot_name == "" or snapshot_dict == "":
                break
            for key, value in snapshot_dict.items():
                container_key_id = key

                for item_value_id in value:
                    if container_key_id == "" or not item_value_id:
                        break

        if(arrangement_id and name and timestamp and item_id
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
    app.run(debug=True)
