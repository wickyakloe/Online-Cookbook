from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/createrecipe")
def create_recipe():
    return render_template("createrecipe.html")

@app.route("/editrecipe")
def edit_recipe():
    return render_template("editrecipe.html")


if __name__ == "__main__":
    app.run(debug=True)
