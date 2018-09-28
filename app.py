from flask import Flask, jsonify, request
import traceback
import random
import datetime
from test_mongo_data import Mdb

app = Flask(__name__)
mdb = Mdb()


def uniqueid():
    seed = random.getrandbits(32)
    while True:
       yield seed
       seed += 1


@app.route("/")
def home_page():
    return "Arrange That!"


@app.route('/arrangement', methods=['POST'])
@app.route('/api/v1/arrangements', methods=['POST'])
def add_arrangement():
    # unique_sequence = uniqueid()
    content = request.json
    try:
        data = {}
        name = content['name']

        is_deleted = content['is_deleted']
        # items = content['item']
        # containers = content['containers']
        # snapshots = content['snapshots']
        items = add_item(content)
        containers = add_container(content)
        snapshots = add_snapshots(content)

        data["_id"] = "a_"+str(next(uniqueid()))
        data["name"] = name
        data["item"] = items
        data["snapshots"] = snapshots
        data["is_deleted"] = is_deleted
        data["containers"] = containers
        data["timestamp"] = datetime.datetime.today().strftime("%a %b %d %X  %Y ")

        mdb.add_arrangement(data)
        return jsonify({"error": '0', 'result': data})

    except Exception as exp:
        print('get_arrangement() :: Got exception: %s' % exp)
        print(traceback.format_exc())
        return jsonify({"error": '1', 'result': 'Some is went wrong!'})


def add_item(content):
    items = content['item']
    response = []
    for item in items:
        name = item['name']
        size = item['size']
        data = {}
        data['_id'] = "i_"+str(next(uniqueid()))
        data['name'] = name
        data['size'] = size

        check = mdb.check_item(name)
        if check:
            result = mdb.get_item_by_name(name)
            response.append(result)
        else:
            result = mdb.add_item(data)
            response.append(result)
    return response


def add_container(content):
    containers = content['containers']
    response = []
    for container in containers:
        data = {}
        name = container['name']
        size = container['size']
        data['_id'] = "c_" + str(next(uniqueid()))
        data['name'] = name
        data['size'] = size
        check = mdb.check_container(name)
        if check:
            result = mdb.get_container_by_name(name)
            response.append(result)
        else:
            result = mdb.add_container(data)
            response.append(result)
    return response


def add_snapshots(content):
    snapshots_data = content['snapshots']
    response = []
    for snap_dict in snapshots_data:
        dict = {}
        name = snap_dict['name']
        snapshots = snap_dict['snapshot']
        data = {}
        for key, value in snapshots.items():
            container = mdb.get_container_by_name(key)
            items = []
            for item in value:
                item = mdb.get_item_by_name(item)
                items.append(item['_id'])
            data[container['_id']] = items

        dict['_id'] = "s_"+ str(next(uniqueid()))
        dict['name'] = name
        dict['snapshot'] = data

        check = mdb.check_snapshot(name)
        if check:
            result = mdb.get_snapshot_by_name(name)
            response.append(result)
        else:
            result = mdb.add_snapshot(dict)
            response.append(result)
    return response


@app.route('/arrangement', methods=['GET'])
@app.route('/api/v1/arrangements', methods=['GET'])
def get_arrangement():
    return mdb.get_all_arrangement()


if __name__ == '__main__':
    app.run(host = 'localhost', port = 8080, debug = True)
