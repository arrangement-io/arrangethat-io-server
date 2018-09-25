from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

@app.route("/")
def home_page():
	return "Arrange That!"
    # user = mongo.db.users.find_one({"_id": user_id})
    # return render_template("index.html",
    #     online_users=online_users)

@app.route("/arrangement", methods=['GET'])
def user_arrangement():
	arrangement_id = request.args.get("id")

	if arrangement_id is null:
		pass
		# return all of the arrangement of that user
		#return mongo.db.arrangement.find({"arrangement_id"})
	else:
		return arrangement_id


# @app.route("/arrangement/id")


# @app.route("/user/<username>")
# def user_profile(username):
#     user = mongo.db.users.find_one_or_404({"_id": username})
#     return render_template("index.html",
#         user=user)

if __name__ == '__main__':
    app.run()
