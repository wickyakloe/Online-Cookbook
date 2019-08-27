import os
from flask import Flask, render_template
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


# Initialize the flask app
app = Flask(__name__)

# Get mongodb URI form env variable
MONGODB_URI = os.getenv("MONGO_URI")
# Set the DB name
app.config["MONGO_DBNAME"] = "online_cookbook"
# Set the Mongo URI
app.config["MONGO_URI"] = MONGODB_URI
# Initialize MongoDB as mongo variable
mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template("index.html", recipes=mongo.db.recipe.find())


@app.route("/view_recipe/<recipe_id>")
def view_recipe(recipe_id):
    the_recipe = mongo.db.recipe.find_one({"_id": ObjectId(recipe_id)})
    return render_template("recipe.html", recipe=the_recipe)


@app.route("/createrecipe")
def create_recipe():
    return render_template("createrecipe.html")


@app.route("/editrecipe")
def edit_recipe():
    return render_template("editrecipe.html")


if __name__ == "__main__":
    app.run(debug=True)
