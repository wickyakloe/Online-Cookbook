import os
import datetime
from flask_login import LoginManager, UserMixin
from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv


# Load the dotenv file
load_dotenv()

# Initialize the flask app
app = Flask(__name__)

# Set the secret key
app.secret_key = os.getenv("SECRET_KEY")

# Get mongodb URI form env variable
MONGODB_URI = os.getenv("MONGO_URI")

# Set the DB name
app.config["MONGO_DBNAME"] = "online_cookbook"

# Set the Mongo URI
app.config["MONGO_URI"] = MONGODB_URI

# Initialize MongoDB as mongo variable
mongo = PyMongo(app)

# Flask-Login LoginManager
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@app.route("/")
def index():
    return render_template("index.html", recipes=mongo.db.recipe.find())


@app.route("/view_recipe/<recipe_id>")
def view_recipe(recipe_id):
    the_recipe = mongo.db.recipe.find_one({"_id": ObjectId(recipe_id)})
    return render_template("recipe.html", recipe=the_recipe)


@app.route("/my_recipes")
def my_recipes():
    return render_template("myrecipes.html", recipes=mongo.db.recipe.find())


@app.route("/create_recipe")
def create_recipe():
    return render_template("createrecipe.html",
                           categories=mongo.db.category.find(),
                           cuisines=mongo.db.cuisine.find())


@app.route("/insert_recipe", methods=["POST"])
def insert_recipe():
    recipes = mongo.db.recipe
    new_recipe = request.form.to_dict()

    # Get all ingredients,cooking tools and steps and put in list
    ingredients = [v for k, v in new_recipe.items() if "ingredient" in k]
    cooking_tools = [v for k, v in new_recipe.items() if "cooking_tool" in k]
    steps = [v for k, v in new_recipe.items() if "step" in k]

    # Insert in database
    recipes.insert_one({
        "date_updated": datetime.datetime.utcnow(),
        "title": request.form.get("recipe_name"),
        "category": request.form.get("category_name"),
        "cuisine": request.form.get("cuisine_name"),
        "image_url": request.form.get("image_url"),
        "description":  request.form.get("description"),
        "ingredients": ingredients,
        "cooking_tools": cooking_tools,
        "steps": steps
    })
    return redirect(url_for("index"))


@app.route("/edit_recipe/<recipe_id>")
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipe.find_one({"_id": ObjectId(recipe_id)})
    return render_template("editrecipe.html", recipe=the_recipe,
                           categories=mongo.db.category.find(),
                           cuisines=mongo.db.cuisine.find())


@app.route("/update_recipe/<recipe_id>", methods=["POST"])
def update_recipe(recipe_id):
    recipe = mongo.db.recipe
    updated_recipe = request.form.to_dict()

    # Get all ingredients,cooking tools and steps and put in list
    ingredients = [v for k, v in updated_recipe.items() if "ingredient" in k]
    cooking_tools = [v for k, v in updated_recipe.items()
                     if "cooking_tool" in k]
    steps = [v for k, v in updated_recipe.items() if "step" in k]

    recipe.update(
        {"_id": ObjectId(recipe_id)},
        {
            "date_updated": datetime.datetime.utcnow(),
            "title": request.form.get("recipe_name"),
            "description":  request.form.get("description"),
            "category": request.form.get("category_name"),
            "cuisine": request.form.get("cuisine_name"),
            "image_url": request.form.get("image_url"),
            "ingredients": ingredients,
            "cooking_tools": cooking_tools,
            "steps": steps
        })
    return redirect(url_for("index"))


@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    mongo.db.recipe.remove({"_id": ObjectId(recipe_id)})
    return redirect(url_for("my_recipes"))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)
