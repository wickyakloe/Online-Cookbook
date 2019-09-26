import os
import datetime
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from user import User
from form import LoginForm, RegisterForm
import pygal

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


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


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
    recipes = mongo.db.recipe.find()
    categories = mongo.db.category.find()
    cuisines = mongo.db.cuisine.find()
    return render_template("index.html", recipes=recipes,
                           categories=categories,
                           cuisines=cuisines)


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
@login_required
def my_recipes():
    """
    The overview page of the created recipes (myrecipes.html)
    by the currently logged in user.
    This page provides the user with an overview
    with the ability to view, edit or delete.
    """
    user = mongo.db.user.find_one(current_user.username)

    return render_template("myrecipes.html", recipes=mongo.db.recipe.find(),
                           user=user)


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
@login_required
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

    # Get current logged in user object
    user = mongo.db.user.find_one(request.form.get("username"))

    # Insert in database
    recipes.insert_one({
        "display_name": user["display_name"],
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
@login_required
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
@login_required
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
@login_required
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


@app.route("/recipe/filter", methods=["GET", "POST"])
def filter():
    recipes = mongo.db.recipe
    categories = mongo.db.category.find()
    cuisines = mongo.db.cuisine.find()
    category = request.args.get("category")
    cuisine = request.args.get("cuisine")
    if category != "Any" and cuisine == "Any":
        filter_category = recipes.find({"category": category})
        return render_template("index.html", recipes=filter_category,
                               categories=categories, cuisines=cuisines)

    if cuisine != "Any" and category == "Any":
        filter_cuisine = recipes.find({"cuisine": cuisine})
        return render_template("index.html", recipes=filter_cuisine,
                               categories=categories, cuisines=cuisines)

    if cuisine != "Any" and category != "Any":
        filter_cuisine = recipes.find({"category": category,
                                       "cuisine": cuisine})
        return render_template("index.html", recipes=filter_cuisine,
                               categories=categories, cuisines=cuisines)

    return redirect(url_for('index'))


@app.route("/dashboard")
def dashboard():
    """
    Show the total recipes per category and cuisine
    in piecharts
    """
    categories = [cat["name"] for cat in mongo.db.category.find()]
    cuisines = [cuis["name"] for cuis in mongo.db.cuisine.find()]
    recipes = mongo.db.recipe
    recipe_cat = []
    recipe_cuis = []
    for item in categories:
        count = recipes.find({"category": item}).count()
        recipe_cat.append([item, count])

    for item in cuisines:
        count = recipes.find({"cuisine": item}).count()
        recipe_cuis.append([item, count])

    pie_chart = pygal.Pie()
    pie_chart.title = 'Recipes by Category'
    for item in recipe_cat:
        pie_chart.add(item[0], item[1])

    chart = pie_chart.render_data_uri()

    pie_chart2 = pygal.Pie()
    pie_chart2.title = 'Recipes by Cuisine'
    for item in recipe_cuis:
        pie_chart2.add(item[0], item[1])

    chart2 = pie_chart2.render_data_uri()

    return render_template("dashboard.html", chart=chart, chart2=chart2)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=os.environ.get('DEBUG'))
