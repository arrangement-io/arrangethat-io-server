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
@app.route('/api/v1/arrangement', methods=['POST'])
def create_arrangement():
    content = request.json
    try:
        data = {}
        name = content['name']

        is_deleted = content['is_deleted']
#         items = add_item(content)
#         containers = add_container(content)
#         snapshots = add_snapshots(content)

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
