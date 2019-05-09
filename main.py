from flask import Flask, request, jsonify, send_from_directory

# PostgreSQL
# import psycopg2
# ---- http://initd.org/psycopg/docs/usage.html ----
# ---- https://devcenter.heroku.com/articles/heroku-postgresql#connecting-in-python ----

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
  return jsonify({'name':'Chef Mike','phone':4031234567,'specialties':['Japanese','Italian'], 'description':'I\'m some dude who cooks stuff'})


# Serves the home page API
@app.route('/api/homepage')
def home_api():
  return jsonify({'topScroller':[{'image':'sushi','text':'Got Sushi?','link':'sushi'}, {'image':'pasta','text':'Got pasta?','link':'pasta'}]})

# Serves the chef list API, after a food type is selected
@app.route('/api/<type>')
def chef_type_list():
  # SELECT chef_name FROM Chefs WHERE specialty LIKE '%{type}%'
  return jsonify([{'name':'Chef Mike','image':'mikepic'}, {'name':'Chef Luke','image':'lukepic'}, {'name':'Chef Bob','image':'bobpic'}])

# Some sort of search bar API
@app.route('/api/search/<search_term>')
def search_field(search_term):
  return 'search results'


if __name__ == '__main__':
  app.run(debug=True)
  # Add to have the server publicly accessable
  # , host= '0.0.0.0'