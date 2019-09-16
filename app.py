import os
import datetime
from flask_login import LoginManager, current_user, login_required, login_user
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from user import User
from form import LoginForm, RegisterForm

# Load the dotenv file
load_dotenv()

# Initialize the flask app
app = Flask(__name__)

# Set the secret key
app.secret_key = os.getenv("SECRET_KEY")

# Set the DB name
app.config["MONGO_DBNAME"] = os.getenv("DBNAME")

# Set the Mongo URI
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

# Initialize MongoDB as mongo variable
mongo = PyMongo(app)

# Flask-Login LoginManager
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(username):
    """
    You will need to provide a user_loader callback.
    This callback is used to reload the user object
    from the user ID stored in the session.
    It should take the unicode ID of a user,
    and return the corresponding user object. For example:

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    It should return None (not raise an exception) if the
    ID is not valid. (In that case, the ID will manually
    be removed from the session and processing will continue.)
    source: https://flask-login.readthedocs.io/en/latest/#how-it-works
    """

    user = mongo.db.user.find_one({"_id": username})
    if not user:
        return None
    return User(user['_id'])


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Opens the login.html page.
    If there is a session cookie the user is logged in directly
    and redirected to the myrecipes.html page.
    If there is no cookie, the entered username and password
    is beinged checked against the database on submit and if correct
    the user is redirected to the myrecipes.html page and if
    incorrect the user is flashed a message and requires to login again
    """

    if current_user.is_authenticated:
        return redirect(url_for("my_recipes"))

    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        username = mongo.db.user.find_one({"_id": form.username.data})
        if username and User.validate_login(username["password"],
                                            form.password.data):
            user_obj = User(username["_id"])
            login_user(user_obj)
            return redirect(request.args.get("next") or url_for("my_recipes"))
        else:
            flash("Invalid username and or password")

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Opens the register.html page.
    When the form is submitted it checks if the
    username and display name already exists if it
    doesn't it inserts the new user into the database
    and redirects the user to createrecipe.html.
    If the username or the display name already exists
    the user is flashed a message.
    """

    user = mongo.db.user
    form = RegisterForm()
    if request.method == "POST" and form.validate_on_submit:
        username = mongo.db.user.find_one({"_id": form.username.data})
        display_name = mongo.db.user.find_one({"display_name":
                                              form.display_name.data})
        if username is None and display_name is None:
            password = request.form.get("password")
            hashPass = generate_password_hash(password)
            user.insert_one({
                "_id": request.form.get("username"),
                "display_name": request.form.get("display_name"),
                "country": request.form.get("country"),
                "password": hashPass
                })
            username = mongo.db.user.find_one({"_id": form.username.data})
            user_obj = User(username["_id"])
            login_user(user_obj)
            return redirect(url_for("create_recipe"))
        elif username:
            flash("Username name already exists")
        elif display_name:
            flash("Display name already exists")

    return render_template("register.html", form=form)


@app.route("/")
def index():
    """
    The landing page of the site (index.html).
    This page provides the user with an overview
    of all the recipes with the ability to view
    a recipe.
    """

    return render_template("index.html", recipes=mongo.db.recipe.find())


@app.route("/view_recipe/<recipe_id>")
def view_recipe(recipe_id):
    """
    The recipe page of the site (recipe.html).
    This page provides the user with detailed
    information of one recipe.
    """

    the_recipe = mongo.db.recipe.find_one({"_id": ObjectId(recipe_id)})
    return render_template("recipe.html", recipe=the_recipe)


@app.route("/my_recipes")
def my_recipes():
    """
    The overview page of the created recipes (myrecipes.html)
    by the currently logged in user.
    This page provides the user with an overview
    with the ability to view, edit or delete.
    """
    return render_template("myrecipes.html", recipes=mongo.db.recipe.find())


@app.route("/create_recipe")
@login_required
def create_recipe():
    """
    The page where the logged in user can create a recipe (createrecipe.html).
    The user is presented with a form to create the recipe.
    """
    return render_template("createrecipe.html",
                           categories=mongo.db.category.find(),
                           cuisines=mongo.db.cuisine.find())


@app.route("/insert_recipe", methods=["POST"])
def insert_recipe():
    """
    When the submit button on the createrecipe.html page is
    clicked this function is called to insert the recipe in
    the database after it has been inserted the user is redirected
    to the landing page index.html.
    """
    recipes = mongo.db.recipe
    new_recipe = request.form.to_dict()

    # Get all ingredients,cooking tools and steps and put in list
    ingredients = [v for k, v in new_recipe.items() if "ingredient" in k]
    cooking_tools = [v for k, v in new_recipe.items() if "cooking_tool" in k]
    steps = [v for k, v in new_recipe.items() if "step" in k]

    # Insert in database
    recipes.insert_one({
        "username": request.form.get("username"),
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
    """
    When the user clicks the edit button on the
    myrecipes.html page, the user will be presented
    with the editrecipe.html page, which is a form
    populated with the data as present in the database
    with the ability to edit every field.
    """
    the_recipe = mongo.db.recipe.find_one({"_id": ObjectId(recipe_id)})
    return render_template("editrecipe.html", recipe=the_recipe,
                           categories=mongo.db.category.find(),
                           cuisines=mongo.db.cuisine.find())


@app.route("/update_recipe/<recipe_id>", methods=["POST"])
def update_recipe(recipe_id):
    """
    When the submit button on the editrecipe.html page is
    clicked this function is called to update the recipe in
    the database after it has been updated the user is redirected
    to the landing page index.html.
    """
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
            "username": request.form.get("username"),
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
    """
    When the user clicks the delete button on the
    myrecipes.html page, the user will be presented
    with a modal to confirm the deletion.
    If confirmed the recipe will be deleted from
    the database.
    """
    mongo.db.recipe.remove({"_id": ObjectId(recipe_id)})
    return redirect(url_for("my_recipes"))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)
