import os
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_uploads import UploadSet, configure_uploads, IMAGES


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

# Flask uploads settings
images = UploadSet("images", IMAGES)
app.config['UPLOADED_IMAGES_DEST'] = 'static/media'
configure_uploads(app, images)


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

    # Use Flask Uploads to save image
    if request.method == "POST" and "image" in request.files:
        filename = images.save(request.files["image"])

    recipes.insert_one({
        "title": request.form.get("recipe_name"),
        "image": filename,
        "description":  request.form.get("description"),
        "ingredients": ingredients,
        "cooking_tools": cooking_tools,
        "steps": steps
    })
    return redirect(url_for("index"))


@app.route("/edit_recipe/<recipe_id>")
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipe.find_one({"_id": ObjectId(recipe_id)})
    return render_template("editrecipe.html", recipe=the_recipe)


@app.route("/update_recipe/<recipe_id>", methods=["POST"])
def update_recipe(recipe_id):
    recipe = mongo.db.recipe
    updated_recipe = request.form.to_dict()
    # Get all ingredients and put in dict
    ingredients = {}
    for ingredientNo, ingredient in updated_recipe.items():
        if "ingredient" in ingredientNo:
            ingredients[ingredientNo] = ingredient
    # Get all cooking_tools and put in dict
    cooking_tools = {}
    for cooking_toolNo, cooking_tool in updated_recipe.items():
        if "cooking_tool" in cooking_toolNo:
            cooking_tools[cooking_toolNo] = cooking_tool
    # Get all steps and put in dict
    steps = {}
    for stepNo, step in updated_recipe.items():
        if "step" in stepNo:
            steps[stepNo] = step
    # Use Flask Uploads to save image
    if request.method == "POST" and "image" in request.files:
        filename = images.save(request.files["image"])

    recipe.update(
        {"_id": ObjectId(recipe_id)},
        {
            "title": request.form.get("recipe_name"),
            "description":  request.form.get("description"),
            "image": filename,
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
            port=int(os.environ.get('PORT')),
            debug=True)
