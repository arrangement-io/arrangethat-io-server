from flask import jsonify
from pymongo import MongoClient
import traceback
from config import *

class Mdb:
    def __init__(self):
        conn_str = "mongodb://%s:%s@%s:%d/%s" % (DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)
        # conn_str = 'mongodb://arrangement_user:arrangement_9pass@ds115963.mlab.com:15963/arrangement_db'
        client = MongoClient(conn_str)
        self.db = client[DB_NAME]\


    ###########################################
    #                   INSERT DATA           #
    ###########################################
    def add_data(self, data, collection):
        mongo_collection = self.db[collection]
        return mongo_collection.insert(data)


    ###########################################
    #        GET ALL ARRANGEMENT DATA         #
    ###########################################
    def get_all_arrangement(self):
        try:
            collection = self.db["arrangement"]
            result = collection.find({})
            ret = []
            for data in result:
                ret.append(data)
        except Exception as exp:
            print("get_all_arrangement() :: Got exception: %s", exp)
            print(traceback.format_exc())
        return jsonify({'arrangements': ret})


    ###########################################
    #    GET SINGLE DATA BY ARRANGEMENT_ID    #
    ###########################################
    def get_data_by_id(self, id):
        try:
            collection = self.db["arrangement"]
            result = collection.find({'_id': id})
            ret = []
            for data in result:
                ret.append(data)
        except Exception as exp:
            print("get_data_by_id() :: Got exception: %s", exp)
            print(traceback.format_exc())
        return jsonify({'arrangement': ret})

    
    ###########################################
    #         CHECK DATA (EXIST OR NOT)       #
    ###########################################
    def check_data(self, query, collection):
        mongo_collection = self.db[collection]
        return mongo_collection.find(query).count() > 0

    
    ###########################################
    #               GET DATA BY NAME          #
    ###########################################
    def get_data_by_name(self, query, collection):
        mongo_collection = self.db[collection]
        response = mongo_collection.find(query)
        ret = {}
        for item in response:
            _id = item['_id']
            name = item['name']
            size = item['size']
            ret['_id'] = _id
            ret['name'] = name
            ret['size'] = size
        return ret        


    def get_snapshot_by_name(self, name):
        try:
            response = self.db.snapshot.find({'name': name})
            ret = {}
            for item in response:
                _id = item['_id']
                name = item['name']
                snapshot = item['snapshot']
                ret['_id'] = _id
                ret['name'] = name
                ret['snapshot'] = snapshot
        except Exception as exp:
            print("get_container_by_name() :: Got exception: %s", exp)
            print(traceback.format_exc())
        return ret


if __name__ == "__main__":
    mdb = Mdb()
