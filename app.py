import os
from flask import Flask, render_template, request, redirect, url_for
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


@app.route("/create_recipe")
def create_recipe():
    return render_template("createrecipe.html")


@app.route("/insert_recipe", methods=["POST"])
def insert_recipe():
    recipes = mongo.db.recipe
    new_recipe = request.form.to_dict()
    # Get all ingredients and put in dict
    ingredients = {}
    for ingredientNo, ingredient in new_recipe.items():
        if "ingredient" in ingredientNo:
            ingredients[ingredientNo] = ingredient
    # Get all cooking_tools and put in dict
    cooking_tools = {}
    for cooking_toolNo, cooking_tool in new_recipe.items():
        if "cooking_tool" in cooking_toolNo:
            cooking_tools[cooking_toolNo] = cooking_tool
    # Get all steps and put in dict
    steps = {}
    for stepNo, step in new_recipe.items():
        if "step" in stepNo:
            steps[stepNo] = step

    recipes.insert_one({
        "recipe_name": request.form.get("recipe_name"),
        "description":  request.form.get("description"),
        "ingredients": ingredients,
        "cooking_tools": cooking_tools,
        "steps": steps
    })

    return redirect(url_for("index"))


@app.route("/editrecipe")
def edit_recipe():
    return render_template("editrecipe.html")


if __name__ == "__main__":
    app.run(debug=True)
