from flask import Flask, jsonify, request
import traceback
import random
import datetime
from test_mongo_data import Mdb
from config import ITEM, CONTAINER, ARRANGEMENT, SNAPSHOT

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
        query = {'name': name}

        check = mdb.check_data(query, ARRANGEMENT)
        if check:
            return jsonify({"error": '1', 'result': 'data already saved!' })
        else:
            mdb.add_data(data, ARRANGEMENT)
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
        query = {'name': name}
        check = mdb.check_data(query, ITEM)
        if check:
            result = mdb.get_data_by_name(query, ITEM)
            response.append(result)
        else:
            mdb.add_data(data, ITEM)
            result = mdb.get_data_by_name(query, ITEM)
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
        query = {'name': name}
        check = mdb.check_data(query, CONTAINER)
        if check:
            result = mdb.get_data_by_name(query, CONTAINER)
            response.append(result)
        else:
            mdb.add_data(data, CONTAINER)
            result = mdb.get_data_by_name(query, CONTAINER)
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
            query1 = {'name':key}
            container = mdb.get_data_by_name(query1, CONTAINER)
            items = []
            for item in value:
                query2 = {'name':item}
                item = mdb.get_data_by_name(query2, ITEM)
                items.append(item['_id'])
            data[container['_id']] = items

        dict['_id'] = "s_"+ str(next(uniqueid()))
        dict['name'] = name
        dict['snapshot'] = data
        query = {'name': name}
        check = mdb.check_data(query, SNAPSHOT)
        if check:
            result = mdb.get_snapshot_by_name(name)
            response.append(result)
        else:
            mdb.add_data(dict, SNAPSHOT)
            result = mdb.get_snapshot_by_name(name)
            response.append(result)
    return response


@app.route('/arrangement', methods=['GET'])
@app.route('/arrangement/<string:arrangement_id>', methods=['GET'])
@app.route('/api/v1/arrangements', methods=['GET'])
@app.route('/api/v1/<string:arrangement_id>', methods=['GET'])
def get_arrangement(arrangement_id=None):
    if arrangement_id is None:
        return mdb.get_all_arrangement()
    else:
        return mdb.get_data_by_id(arrangement_id)


if __name__ == '__main__':
    app.run(host = 'localhost', port = 8080, debug = True)
