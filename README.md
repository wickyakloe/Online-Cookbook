# Project Online Cookbook

Create an online cookbook to Find and share recipes.

Table of Content:

- [UX](#ux)
  - [Front-End Mockup](#front-end-mockup)
- [Database](#database)
  - [MongoDB](#mongodb)
    - [Creating the Database](#creating-the-database)
    - [ER Diagram](#er-diagram)
- [Features](#features)
  - [Existing Features](#existing-features)
  - [Features Left to Implement](#features-left-to-implement)
- [Technologies Used](#technologies-used)
- [Testing](#testing)
- [Deployment](#deployment)
  - [Heroku](#heroku)
- [Credits](#credits)
- [Content](#content)
- [Media](#media)
- [Acknowledgements](#acknowledgements)

---

- Site owner's goal:
Promote a brand of cooking tools.

- Potential features to include:
  - Create a web application that allows users to store and easily access cooking recipes. Recipes would include fields such as ingredients, preparation steps, required tools, cuisine, etc.

  - Create the backend code and frontend form(s) to allow users to add new recipes to the site, edit them and delete them.

  - Create the backend and frontend functionality for users to locate recipes based on the recipe's fields. You may choose to create a full search functionality, or just a directory of recipes.

  - Provide results in a manner that is visually appealing and user friendly.

- Advanced potential feature (nice-to-have):

  - Build upon the required tools field to promote your brand of kitchen tools (e.g. oven, pressure cooker, etc…).

   - Create a dashboard to provide some statistics about all the recipes.
 
## UX
 
<!-- Use this section to provide insight into your UX process, focusing on who this website is for, what it is that they want to achieve and how your project is the best way to help them achieve these things.

In particular, as part of this section we recommend that you provide a list of User Stories, with the following general structure:
- As a user type, I want to perform an action, so that I can achieve a goal.

This section is also where you would share links to any wireframes, mockups, diagrams etc. that you created as part of the design process. These files should themselves either be included in the project itself (in an separate directory), or just hosted elsewhere online and can be in any format that is viewable inside the browser. -->

- Mockup: View the mockup [here](https://wickyakloe.github.io/Online-Cookbook/mockup/)

- Color choices:
  - Primary color: ![Primary Color](https://raw.githubusercontent.com/wickyakloe/Online-Cookbook/master/materialize_primary_color.png "Materialize blue-grey darken-3")
  - Secondary color: ![Secondary Color](https://raw.githubusercontent.com/wickyakloe/Online-Cookbook/master/materialize_secondary_color.png "Materialize yellow darken-3")

## Database

### MongoDB

We will be using the free tier of MongoDB Atlas which is a cloud MongoDB service. You can find more information [here](https://www.mongodb.com/cloud/atlas)

#### Creating the Database

1. Create a free account on the mongodb [website](https://www.mongodb.com/) and [sign in].(https://cloud.mongodb.com/user#/atlas/login)

2. Create a free tier cluster, database and a mongodb user for your cluster. You can follow the instructions [here](https://docs.atlas.mongodb.com/getting-started/#deploy-a-free-tier-cluster) how to do this.

3. In your database create the following collections according to the entity diagram below
    - user
    - recipe
    - category

### ER Diagram

The database will be constructed according to the following Entity Relationship diagram:

Inline-style: 
![ER-Diagram](https://github.com/wickyakloe/Online-Cookbook/raw/master/ER_Diagram_Project_3.jpg "ER-Diagram Online-Cookbook")

Click [here](https://www.draw.io/?lightbox=1&highlight=0000ff&layers=1&nav=1&title=ER_Diagram_Project_3.drawio#Uhttps%3A%2F%2Fraw.githubusercontent.com%2Fwickyakloe%2FOnline-Cookbook%2Fmaster%2FER_Diagram_Project_3.drawio) to view the diagram in your browser.

*This ER-Diagram is made using [draw.io](https://www.draw.io).*

## Features

<!-- In this section, you should go over the different parts of your project, and describe each in a sentence or so.
 
### Existing Features
- Feature 1 - allows users X to achieve Y, by having them fill out Z
- ...

For some/all of your features, you may choose to reference the specific project files that implement them, although this is entirely optional.

In addition, you may also use this section to discuss plans for additional features to be implemented in the future:

### Features Left to Implement
- Another feature idea -->

## Technologies Used

- HTML
- CSS
- Javascript
- Python3
- MongoDB

Modules/Frameworks:

- JQuery
- Bootstrap/Materialize?
- Flask

## Testing

<!-- In this section, you need to convince the assessor that you have conducted enough testing to legitimately believe that the site works well. Essentially, in this part you will want to go over all of your user stories from the UX section and ensure that they all work as intended, with the project providing an easy and straightforward way for the users to achieve their goals.

Whenever it is feasible, prefer to automate your tests, and if you've done so, provide a brief explanation of your approach, link to the test file(s) and explain how to run them.

For any scenarios that have not been automated, test the user stories manually and provide as much detail as is relevant. A particularly useful form for describing your testing process is via scenarios, such as:

1. Contact form:
    1. Go to the "Contact Us" page
    2. Try to submit the empty form and verify that an error message about the required fields appears
    3. Try to submit the form with an invalid email address and verify that a relevant error message appears
    4. Try to submit the form with all inputs valid and verify that a success message appears.

In addition, you should mention in this section how your project looks and works on different browsers and screen sizes.

You should also mention in this section any interesting bugs or problems you discovered during your testing, even if you haven't addressed them yet.

If this section grows too long, you may want to split it off into a separate file and link to it from here. -->

unitest python
jasmin ?
python module?

## Deployment

<!-- This section should describe the process you went through to deploy the project to a hosting platform (e.g. GitHub Pages or Heroku).

In particular, you should provide all details of the differences between the deployed version and the development version, if any, including:
- Different values for environment variables (Heroku Config Vars)?
- Different configuration files?
- Separate git branch?

In addition, if it is not obvious, you should also describe how to run your code locally. -->

### Local deployment

*Instructions for linux*

1. Make sure you have [python3](https://www.python.org/) installed
2. Install virtualenv with pip

```bash
#On linux you first need to install pip
sudo apt install python3-pip

#Then u can install virtualenv using pip3
sudo pip3 install virtualenv
```

3.Create a python virtualenv and activate it

```bash
#Replace online-cookbook with your directory name
virtualenv online-cookbook

#activate the virtualenv
source online-cookbook/bin/activate

#deactive the virualenv
deactivate
```

4.Install Flask in the virutalenv

```bash
pip3 install Flask
```

5.Clone this repository and put the contents in your virtualenv

6.Run the app.py

```bash
python3 app.py
```

### Heroku

How to deploy to heroku here

## Credits

### Content
- The text for section Y was copied from the [Wikipedia article Z](https://en.wikipedia.org/wiki/Z)

### Media
- The icon used as logo in the navbar is from [iconstore](https://iconstore.co/icons/tasty-icons-free/)

### Acknowledgements

- I received inspiration for this project from X