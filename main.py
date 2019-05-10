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
@app.route('/api/chef', methods=['GET'])
def chef_api():
    chef_name = request.get_json()['chef']
    cur.execute(f"SELECT * FROM Chef WHERE name = '{chef_name}'")
    currChef = cur.fetchone()
    return jsonify({'name': currChef[1], 'phone': currChef[4], 'specialties': [ft for ft in currChef[3].split(', ')], 'description': currChef[5]})


# Serves the home page API
@app.route('/api/homepage', methods=['GET'])
def home_api():

    # Top box
    topScroller = []
    cur.execute("SELECT COUNT(*) FROM food_type")
    count = int(cur.fetchall()[0][0])
    cur.execute(
        f"SELECT food_type,picture FROM food_type OFFSET {random.randint(1,count)} LIMIT 5")
    for food_name, picture in cur.fetchall():
        topScroller.append({'foodName': food_name, 'picture': picture})

    # Food Types
    food_types = []
    cur.execute(f"SELECT food_type,picture FROM food_type")
    for food_name, picture in cur.fetchall():
        food_types.append({'foodName': food_name, 'picture': picture})

    # Chefs
    chefs = []
    cur.execute(f"SELECT name, picture FROM chef")
    chef_list = random.sample(cur.fetchall(), 6)
    for name, picture in chef_list:
        chefs.append({'name': name, 'picture': picture})

    return jsonify({'topScroller': topScroller, 'foodTypes': food_types, 'chefs': chefs})

# Serves the chef list API, after a food type is selected
@app.route('/api/foodtype', methods=['GET'])
def chef_type_list():
    food_type = request.get_json()['foodtype']
    chefs = []
    cur.execute(f"SELECT name, picture FROM chef WHERE specialty LIKE '%{food_type.lower()}%'")
    for chef in cur.fetchall():
      chefs.append({'name':chef[0], 'picture':chef[1]})
    return jsonify(chefs)

# Some sort of search bar API
@app.route('/api/search/', methods=['GET'])
def search_field():
    search_term = request.get_json()['searchterm']

    # Search food types
    cur.execute(f"SELECT food_type, picture FROM food_type WHERE food_type LIKE '%{search_term.lower()}%'")
    food_type = [{"name":name,"picture":picture} for name, picture in cur.fetchall()]

    # Search chefs
    cur.execute(f"SELECT name, picture FROM chef WHERE name LIKE '%{search_term.lower()}%'")
    chefs = [{"name":name,"picture":picture} for name, picture in cur.fetchall()]
    return jsonify({"foodTypes":food_type,"chefs":chefs})


if __name__ == '__main__':
    app.run(debug=True)
    # Add to have the server publicly accessable
    # , host= '0.0.0.0'
