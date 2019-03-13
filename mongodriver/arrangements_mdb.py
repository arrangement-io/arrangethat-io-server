from flask import jsonify
from pymongo import MongoClient
import traceback
from config import *

class ArrangementsMDB(object):
    def __init__(self):
        conn_str = "mongodb://%s:%s@%s:%d/%s" % (DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)
        client = MongoClient(conn_str)
        self.db = client[DB_NAME]
        self.collection = self.db['arrangement']


    ###########################################
    #               Add Arrangement           #
    ###########################################
    def add_arrangement(self, arrangement):
        return self.collection.insert(arrangement)

    ###########################################
    #               Replace Arrangement       #
    ###########################################
    def replace_arrangement(self, arrangement):
        self.collection.replace_one({"_id": arrangement["_id"]}, arrangement)

    ###########################################
    #              GET ALL ARRANGEMENT DATA   #
    ###########################################
    def get_all_arrangements(self):
        try:
            return list(self.collection.find({}))
        except Exception as exp:
            print("get_all_arrangements() :: Got exception: %s", exp)
            print(traceback.format_exc())
        return jsonify({"error: %s": exp})



    def get_all_arrangements_by_user(self, user):
        try:
            return list(self.collection.find({"owner": user}))
        except Exception as exp:
            print("get_all_arrangements_by_user() :: Got exception: %s", exp)
            print(traceback.format_exc())
        return jsonify({"error: %s": exp})

    ###########################################
    #    GET SINGLE DATA BY ARRANGEMENT_ID    #
    ###########################################
    def get_arrangement_by_id(self, arrangement_id):
        try:
            result = self.collection.find({"_id": arrangement_id})
            response = []
            for arrangement in result:
                response.append(arrangement)

            return response
        except Exception as exp:
            print("get_arrangement_by_id():: Got exception: %s", exp)
            print(traceback.format_exc())
            return jsonify({"error %s: ", exp})

    ###########################################
    #         CHECK ARRANGEMENT EXISTS        #
    ###########################################
    def check_arrangement_exists(self, arrangement):
        return self.collection.find({"_id": arrangement["_id"]}).count() > 0


if __name__ == "__main__":
    mdb = ArrangementsMDB()
