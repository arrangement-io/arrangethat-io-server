from flask import jsonify
from pymongo import MongoClient
import traceback
from config import *


class Mdb:
    def __init__(self):
        conn_str = "mongodb://%s:%s@%s:%d/%s" % (DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)
        # conn_str = 'mongodb://arrangement_user:arrangement_9pass@ds115963.mlab.com:15963/arrangement_db'
        client = MongoClient(conn_str)
        self.db = client[DB_NAME]

    def add_arrangement(self, data):
        try:
            self.db.arrangement.insert(data)
        except Exception as exp:
            print("add_arrangement() :: Got exception: %s", exp)
            print(traceback.format_exc())

    def add_item(self, data):
        try:
            # id =  self.db.item.insert(data)
            response = self.db.item.find({'_id': self.db.item.insert(data)})
            ret = {}
            for item in response:
                _id = item['_id']
                name = item['name']
                size = item['size']

                ret['_id'] = _id
                ret['name'] = name
                ret['size'] = size
        except Exception as exp:
            print("add_item() :: Got exception: %s", exp)
            print(traceback.format_exc())
        return ret

    def add_container(self, data):
        try:
            # id =  self.db.container.insert(data)
            response = self.db.container.find({'_id': self.db.container.insert(data)})
            ret = {}
            for container in response:
                _id = container['_id']
                name = container['name']
                size = container['size']
                ret['_id'] = _id
                ret['name'] = name
                ret['size'] = size
        except Exception as exp:
            print("add_container() :: Got exception: %s", exp)
            print(traceback.format_exc())
        return ret

    def add_snapshot(self, data):
        self.db.snapshot.insert(data)


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

    def check_item(self, name):
        return self.db.item.find({'name': name}).count() > 0

    def check_container(self, name):
        return self.db.container.find({'name': name}).count() > 0

    def check_snapshot(self, name):
        return self.db.snapshot.find({'name': name}).count() > 0



    def get_item_by_name(self, name):
        try:
            response = self.db.item.find({'name': name})
            ret = {}
            for item in response:
                _id = item['_id']
                name = item['name']
                size = item['size']
                ret['_id'] = _id
                ret['name'] = name
                ret['size'] = size

        except Exception as exp:
            print("get_item_by_name() :: Got exception: %s", exp)
            print(traceback.format_exc())
        return ret

    def get_container_by_name(self, name):
        try:
            response = self.db.container.find({'name': name})
            ret = {}
            for item in response:
                _id = item['_id']
                name = item['name']
                size = item['size']
                ret['_id'] = _id
                ret['name'] = name
                ret['size'] = size
        except Exception as exp:
            print("get_container_by_name() :: Got exception: %s", exp)
            print(traceback.format_exc())
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
