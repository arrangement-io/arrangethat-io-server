from flask import jsonify
from pymongo import MongoClient
import traceback
from config import *

class UsersMDB(object):
    def __init__(self):
        conn_str = "mongodb://%s:%s@%s:%d/%s" % (DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)
        client = MongoClient(conn_str)
        self.db = client[DB_NAME]
        self.collection = self.db['users']
    
    """ Add a user """
    def add_user(self, user):
        return self.collection.update({"googleId":user['googleId']}, user, upsert=True)

    """ Get all the users """
    def get_all_users(self):
        try:
            # Remove the bson id and email
            return list(self.collection.find({},{"_id":0, "email":0}))    
        except Exception as exp:
            print("get_all_users() :: Got exception: %s", exp)
            print(traceback.format_exc())
        return jsonify({"error: %s": exp})
    
