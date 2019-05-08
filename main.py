from flask import Flask, request, jsonify, send_from_directory

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
  return jsonify({'topScroller':[{'image':'images/sushi','text':'Got Sushi?','link':'sushi'}, {'image':'images/pasta','text':'Got pasta?','link':'pasta'}]})

# Serves the chef list API, after a food type is selected
@app.route('/api/<type>')
def chef_type_list():
  # SELECT chef_name FROM Chefs WHERE specialty LIKE '%{type}%'
  return jsonify(['Chef Mike', 'Chef Luke', 'Chef Bob'])

# Serves images
# May not be needed??
@app.route('/images/<path>')
def returnIcons(path):
  return send_from_directory('images/',path)


if __name__ == '__main__':
  app.run(debug=True)
  # Add to have the server publicly accessable
  # , host= '0.0.0.0'