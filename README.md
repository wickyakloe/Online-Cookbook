# Project Online Cookbook

Online cookbook to Find and Share recipes.

![ResponsiveView](https://raw.githubusercontent.com/wickyakloe/Online-Cookbook/master/assets/responsiveView.png "Mobile and Desktop View")

Table of Content:

- [Features](#features)
- [UX](#ux)
  - [Front-End Mockup](#front-end-mockup)
- [Database](#database)
  - [MongoDB](#mongodb)
    - [Creating the Database](#creating-the-database)
    - [ER Diagram](#er-diagram)
- [Technologies Used](#technologies-used)
- [Testing](#testing)
- [Deployment](#deployment)
  - [Heroku](#heroku)
  - [Local](#local-deployment)
- [Credits](#credits)
- [Media](#media)

---
## Features

- Site owner's goal:
Allow users to share recipes

- Potential features to include:
  - Create a web application that allows users to store and easily access cooking recipes. Recipes would include fields such as ingredients, preparation steps, required tools, cuisine, etc.

  - Create the backend code and frontend form(s) to allow users to add new recipes to the site, edit them and delete them.

  - Create the backend and frontend functionality for users to locate recipes based on the recipe's fields. You may choose to create a full search functionality, or just a directory of recipes.

  - Provide results in a manner that is visually appealing and user friendly.

- Advanced potential feature (nice-to-have):

   - Create a dashboard to provide some statistics about all the recipes.
 
## UX

See the initial mockup [here](https://wickyakloe.github.io/Online-Cookbook/mockup/)

Color choices:

| Primary        | Secondary  |
| ------------- | ----- |
| ![Primary Color](https://raw.githubusercontent.com/wickyakloe/Online-Cookbook/master/assets/materialize_primary_color.png "Materialize blue-grey darken-3")     | ![Secondary Color](https://raw.githubusercontent.com/wickyakloe/Online-Cookbook/master/assets/materialize_secondary_color.png "Materialize yellow darken-3") |

## Database

### MongoDB

We will be using the free tier of MongoDB Atlas which is a cloud MongoDB service. You can find more information [here](https://www.mongodb.com/cloud/atlas)

#### Creating the Database

1. Create a free account on the mongodb [website](https://www.mongodb.com/) and [sign in].(https://cloud.mongodb.com/user#/atlas/login)

2. Create a free tier cluster, database and a mongodb user for your cluster. You can follow the instructions [here](https://docs.atlas.mongodb.com/getting-started/#deploy-a-free-tier-cluster) how to do this.

3. In your database the following collections will be created by the application:
    - user
    - recipe

And the following collections need to be manually created:
 - category ( as per ER diagram below )
 - cuisine ( as per ER diagram below )
 - countries ( import [this](https://github.com/ozlerhakan/mongodb-json-files/blob/master/datasets/countries-small.json
) json file )


### ER Diagram

The database will be constructed according to the following Entity Relationship diagram:

![ER-Diagram](https://github.com/wickyakloe/Online-Cookbook/raw/master/assets/ER_Diagram_Project_3.jpg "ER-Diagram Online-Cookbook")

Click [here](https://www.draw.io/?lightbox=1&highlight=0000ff&layers=1&nav=1&title=ER_Diagram_Project_3.drawio#Uhttps%3A%2F%2Fraw.githubusercontent.com%2Fwickyakloe%2FOnline-Cookbook%2Fmaster%2Fassets%2FER_Diagram_Project_3.drawio) to view the diagram in your browser.

*This ER-Diagram is made using [draw.io](https://www.draw.io).*

## Technologies Used

- HTML
- CSS
- Javascript
- Python3
- MongoDB

Modules/Frameworks:

- JQuery
- Materialize
- Flask
- Flask-Login
- Flask-WTF
- Python unitttest

## Testing

The Flask app is tested using pythons [unittest](https://docs.python.org/3/library/unittest.html) module in combination with the [coverage](https://coverage.readthedocs.io/en/v4.5.x/) module for seeing the code coverage of the unit tests.

Coverage:

| Name     | Stmts | Miss | Cover |
|----------|-------|------|-------|
| app.py   | 142   | 44   | 69%   |
| form.py  | 9     | 0    | 100%  |
| tests.py | 75    | 0    | 100%  |
| user.py  | 15    | 3    | 80%   |
| TOTAL     | 241   | 47   | 80%   |

Click here for > [full coverage report](https://wickyakloe.github.io/Online-Cookbook/assets/htmlcov/).

You can run the tests manually with the following command:

```code
python3 -m unittest
```

Using the coverage module(
add the -m flag to see which lines are not being tested )

```code
# To run the tests.
coverage run tests.py

# To get a report in plain view
coverage report -m *.py

# To generate a pretty HTML report
coverage html *.py
```


## Deployment

### Heroku

This application is deployed to heroku here [http://wickz-recipe-share.herokuapp.com/](http://wickz-recipe-share.herokuapp.com/).

When deploying to heroku use the following config vars

| Variable        | Value  |
| --------------- | ------ |
|DEBUG| True or Empty |
|MONGO_URI| MONGO connection link |
|DBNAME| MONGO DB name |
|IP| 0.0.0.0 |
|PORT| 5000 |
|SECRECT_KEY| yoursecretkey |

### Local deployment

*Instructions for linux*


1.Make sure you have [python3](https://www.python.org/) installed

2.Install virtualenv with pip

```bash
#On linux you first need to install pip
sudo apt install python3-pip

#Then u can install virtualenv using pip3
sudo pip3 install virtualenv
```

3.Clone this repository and put the contents in your virtualenv

4.Create a python virtualenv and activate it

```bash
#Replace online-cookbook with your directory name
virtualenv online-cookbook

#activate the virtualenv
source online-cookbook/bin/activate

#deactive the virualenv
deactivate
```

5.Install the packages in the virutalenv

```bash
pip3 install -r requirements.txt
```

6.Create the following .env file in the root of the directory
and fill in the values.

```env
# See https://github.com/theskumar/python-dotenv for instructions

# Connection link to MONGODB
MONGO_URI = ""

# DB to connect to
DBNAME= ""

# Flask secret key
SECRET_KEY = ""

# Set to empty for false i.e. DEBUG = ""
DEBUG = "True"
```

7.Run the app.py

```bash
python3 app.py
```

## Credits

- For unittesting examples and usage > https://www.patricksoftwareblog.com/unit-testing-a-flask-application/

- Flask-Login example > https://github.com/boh717/FlaskLogin-and-pymongo

- Countries collections > https://github.com/ozlerhakan/mongodb-json-files/blob/master/datasets/countries-small.json

### Media
- The icon used as logo in the navbar is from [iconstore](https://iconstore.co/icons/tasty-icons-free/)
- Current displayed 'test' recipes are from [jamie oliver](https://www.jamieoliver.com/) website and from [allrecipes](https://www.allrecipes.com/)
