import datetime
from flask import Flask
from flask_jwt_extended import JWTManager
from pymongo import MongoClient

app = Flask(__name__)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'Your_Secret_Key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)

connection_url = 'mongodb+srv://sloovi:sloovi@template.t6v0y.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(connection_url)

# Database
Database = client.get_database('template')
# Table
users_collection = Database.Users
template_collection = Database.templates


from api import routes