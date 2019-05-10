from flask import Flask, request, jsonify, send_from_directory
import random

# PostgreSQL
# ---- http://initd.org/psycopg/docs/usage.html ----
# ---- https://devcenter.heroku.com/articles/heroku-postgresql#connecting-in-python ----
import psycopg2
import json
data = json.load(open('SecretFile.json', 'r'))
conn = psycopg2.connect(
    dbname=data['dbname'], user=data['user'], password=data['password'], host=data['host'])
cur = conn.cursor()

# Auth0
# from jose import jwt
# import json
# from six.moves.urllib.request import urlopen
# from functools import wraps
# ---- https://auth0.com/docs/quickstart/backend/python ----
# ---- https://devcenter.heroku.com/articles/auth0 ----

# Cloudinary
# Pass publicId to react and have react fetch and compile.
# Store publicId in DB with chef/food type
# https://cloudinary.com/documentation/react_integration

# Serves react build
app = Flask(__name__)

# Serves the chef profile API
@app.route('/api/chef/<chef_name>')
def chef_api(chef_name):
    # SELECT * FROM Chefs WHERE name = {chef_name}
    return jsonify({'name': 'Chef Mike', 'phone': 4031234567, 'specialties': ['Japanese', 'Italian'], 'description': 'I\'m some dude who cooks stuff'})


# Serves the home page API
@app.route('/api/homepage')
def home_api():

    # Top box
    topScroller = []
    cur.execute("SELECT COUNT(*) FROM food_type")
    count = int(cur.fetchall()[0][0])
    cur.execute(
        f"SELECT food_type,picture FROM food_type OFFSET {random.randint(1,count)} LIMIT 5")
    for result in cur.fetchall():
        topScroller.append({'foodName': result[0], 'picture': result[1]})

    # Food Types
    food_types = []
    cur.execute(f"SELECT food_type,picture FROM food_type")
    for result in cur.fetchall():
        food_types.append({'foodName': result[0], 'picture': result[1]})

    # Chefs
    chefs = []
    cur.execute(f"SELECT * FROM chef")
    chef_list = random.sample(cur.fetchall(),6)
    for result in chef_list:
        chefs.append({'name': result[1], 'picture': result[2], 'specialties': [ft for ft in result[3].split(', ')], 'phone_num': result[4], 'description': result[5]})

    return jsonify({'topScroller': topScroller, 'foodTypes': food_types, 'chefs': chefs})

# Serves the chef list API, after a food type is selected
@app.route('/api/<type>')
def chef_type_list():
    # SELECT chef_name FROM Chefs WHERE specialty LIKE '%{type}%'
    return jsonify([{'name': 'Chef Mike', 'image': 'mikepic'}, {'name': 'Chef Luke', 'image': 'lukepic'}, {'name': 'Chef Bob', 'image': 'bobpic'}])

# Some sort of search bar API
@app.route('/api/search/<search_term>')
def search_field(search_term):
    return 'search results'


if __name__ == '__main__':
    app.run(debug=True)
    # Add to have the server publicly accessable
    # , host= '0.0.0.0'
