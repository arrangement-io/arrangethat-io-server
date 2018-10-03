from flask import jsonify
from pymongo import MongoClient
import traceback
from config import *

class Mdb:
    def __init__(self):
        conn_str = "mongodb://%s:%s@%s:%d/%s" % (DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)
        client = MongoClient(conn_str)
        self.db = client[DB_NAME]


    ###########################################
    #               Add Arrangement           #
    ###########################################
    def add_arrangement(self, arrangement):
        return self.db["arrangement"].insert(arrangement)

    ###########################################
    #               Replace Arrangement       #
    ###########################################
    def replace_arrangement(self, arrangement):
        self.db["arrangement"].replace_one({"id": arrangement["id"]}, arrangement)

    ###########################################
    #              GET ALL ARRANGEMENT DATA   #
    ###########################################
    def get_all_arrangements(self):
        try:
            return list(self.db["arrangement"].find({}))
        except Exception as exp:
            print("get_all_arrangements() :: Got exception: %s", exp)
            print(traceback.format_exc())
        return jsonify({"error: %s": exp})

    ###########################################
    #    GET SINGLE DATA BY ARRANGEMENT_ID    #
    ###########################################
    def get_arrangement_by_id(self, id):
        try:
            result = self.db["arrangement"].find({"id": id})
            response = []
            for data in result:
                response.append(data)
            if len(response) == 1:
                return jsonify({"arrangement": response[0]})
            else:
                return jsonify({"arrangement": "no arrangement found"})
        except Exception as exp:
            print("get_arrangement_by_id():: Got exception: %s", exp)
            print(traceback.format_exc())
            return jsonify({"error %s: ", exp})

    ###########################################
    #         CHECK ARRANGEMENT EXISTS        #
    ###########################################
    def check_arrangement_exists(self, arrangement):
        return self.db["arrangement"].find({"id": arrangement["id"]}).count() > 0
    

if __name__ == "__main__":
    mdb = Mdb()
