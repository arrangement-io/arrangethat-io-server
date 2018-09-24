from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

@app.route("/")
def home_page():
    online_users = mongo.db.users.find({"online": True})
    return render_template("index.html",
        online_users=online_users)

@app.route("/arrangement", methods=['GET'])
def user_arrangement():
	arrangement_id = request.args.get("id")
	if null:
		# 
		# return all of the arrangement of that user
		return mongo.db.arrangement.find({"arrangement_id"})
	else:
		return arrangement_id


# @app.route("/arrangement/id")


@app.route("/user/<username>")
def user_profile(username):
    user = mongo.db.users.find_one_or_404({"_id": username})
    return render_template("user.html",
        user=user)

if __name__ == '__main__':
    app.run()
