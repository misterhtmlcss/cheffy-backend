import psycopg2
import json
data = json.load(open('SecretFile.json', 'r'))
conn = psycopg2.connect(dbname=data['dbname'], user=data['user'], password=data['password'], host=data['host'])
cur = conn.cursor()

from faker import Faker
import random
fake = Faker()

import re

# Tasks to do:
clear_tables = False
create_databases = False
populate_database = False

# How many of each:
chef_num_range = [15,20]
customer_num_range = [30,40]

if clear_tables:
  print("Are you sure you want to drop all tables? YES/NO")
  if input().upper() == "YES":
    cur.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    for table in cur.fetchall():
      print(f"Dropping table: {table[0]}")
      cur.execute(f"DROP TABLE {table[0]};")

if create_databases:
  cur.execute("""CREATE TABLE Chef(
    Chef_Id SERIAL PRIMARY KEY,
    Name TEXT NOT NULL,
    Picture TEXT,
    Specialty TEXT NOT NULL,
    Phone_Num TEXT,
    DESCRIPTION TEXT
  );""")
  print("Made Chef table")

  cur.execute("""CREATE TABLE Customer(
    User_Id SERIAL PRIMARY KEY,
    Auth0_Id INT,
    Username TEXT NOT NULL,
    Picture TEXT
  );""")
  print("Made Customer table")

  cur.execute("""CREATE TABLE Food_Type(
    Food_Id SERIAL PRIMARY KEY,
    Food_Type TEXT NOT NULL,
    Picture TEXT
  );""")
  print("Made Food_Type table")

  cur.execute("""CREATE TABLE Comment(
    Chef_Id INT NOT NULL,
    Username TEXT NOT NULL,
    Comment TEXT NOT NULL
  );""")
  print("Made Comment table")

if populate_database:
  print("Would you like to clear tables first? YES/NO")
  if input().upper() == "YES":
    cur.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    for table in cur.fetchall():
      print(f"Clearing table: {table[0]}")
      cur.execute(f"TRUNCATE TABLE {table[0]};")


  print("Populating Food_Type table...")
  food_types = ["algerian", "argentinan", "australian", "brazilian", "cameroonian", "canadian", "chilean", "chinese", "cuban", "czechian", "egyptian", "ethiopian", "franch", "german", "ghanese", "greek", "guatemalan", "haitian", "hungarian", "indian", "indonesian", "iranian", "iraqi", "irish", "israeli", "italian", "jamaican", "japanese", "kazakhstani", "kenyan", "korean", "lebanese", "liberian", "mexican", "moroccan", "mozambiquese", "nigerian", "pakistani", "peruvian", "philippino", "polish", "russian", "saudi arabian", "slovenian", "south african", "spanish", "swedish", "tanzanian", "thai", "turkish", "ukrainian", "british", "american", "vietnamese", "zimbabwean"]
  for food in food_types:
    cur.execute(f"INSERT INTO Food_Type(Food_Type, Picture) VALUES('{food}','{re.sub('[^A-Za-z]','',food).lower()}');")


  print("Populating Chef table...")
  for num in range(random.randint(chef_num_range[0],chef_num_range[1])):
    name = fake.name()
    cur.execute(f"INSERT INTO Chef(name, picture, specialty, phone_num) VALUES ('{name}', '{re.sub('[^A-Za-z]','',name).lower()}','{', '.join(random.sample(food_types,random.randint(1,3)))}','{fake.phone_number()}')")
  
  
  print("Populating Customer table...")
  for num in range(random.randint(customer_num_range[0],customer_num_range[1])):
    cur.execute(f"INSERT INTO Customer(username) VALUES ('{fake.user_name()}');")
  
  
  print("Populating Comment table...")
  cur.execute("SELECT COUNT(*) FROM customer")
  num_customers = cur.fetchone()
  cur.execute("SELECT Chef_Id FROM chef")
  for chef in cur.fetchall():
    for num in range(random.randint(10,15)):
      cur.execute(f"INSERT INTO comment(Chef_Id,Username,Comment) VALUES ({chef[0]},(SELECT Username FROM customer WHERE User_Id = {random.randint(1,int(num_customers[0]))}),'{''.join(fake.paragraphs())}');")
    


conn.commit()

cur.close()
conn.close()