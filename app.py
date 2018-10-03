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
def save_arrangement():
    arrangement = request.json
    # TODO: validate_arrangement(arrangement) 
    # name = arrangement['name']
    # query = {'name': name}
    arrangement_exists = mdb.check_arrangement_exists(arrangement)
    if arrangement_exists:
        mdb.replace_arrangement(arrangement)
    else:
        mdb.add_arrangement(arrangement)
    return jsonify(arrangement)

@app.route('/arrangement', methods=['GET'])
@app.route('/arrangement/<string:arrangement_id>', methods=['GET'])
@app.route('/api/v1/arrangements', methods=['GET'])
@app.route('/api/v1/<string:arrangement_id>', methods=['GET'])
def get_arrangement(arrangement_id=None):
    if arrangement_id is None:
        return jsonify(mdb.get_all_arrangement())
    else:
        return jsonify(mdb.get_arrangement_by_id(arrangement_id))


if __name__ == '__main__':
    app.run(debug = True)
