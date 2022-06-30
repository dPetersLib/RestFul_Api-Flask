import hashlib
import datetime
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo import MongoClient
import pymongo

app = Flask(__name__)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'Your_Secret_Key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)

connection_url = 'mongodb+srv://sloovi:sloovi@template.t6v0y.mongodb.net/?retryWrites=true&w=majority'
client = pymongo.MongoClient(connection_url)

# Database
Database = client.get_database('template')
# Table
users_collection = Database.Users
template_collection = Database.template


@app.route("/api/v1/register", methods=["POST"])
def register():
    new_user = request.get_json()  # store the json body request
    new_user["password"] = hashlib.sha256(
        new_user["password"].encode("utf-8")).hexdigest()  # encrpt password
    doc = users_collection.find_one(
        {"email": new_user["email"]})  # check if user exist
    if not doc:
        users_collection.insert_one(new_user)
        return jsonify({'msg': 'User created successfully'}), 201
    else:
        return jsonify({'msg': 'Username already exists'}), 409


@app.route("/api/v1/login", methods=["POST"])
def login():
    login_details = request.get_json()  # store the json body request
    user_from_db = users_collection.find_one(
        {'email': login_details['email']})  # search for user in database

    if user_from_db:
        encrpted_password = hashlib.sha256(
            login_details['password'].encode("utf-8")).hexdigest()
        if encrpted_password == user_from_db['password']:
            access_token = create_access_token(
                identity=user_from_db['email'])  # create jwt token
            return jsonify(access_token=access_token), 200

    return jsonify({'msg': 'The username or password is incorrect'}), 401


@app.route("/api/v1/template", methods=["GET"])
@jwt_required()
def get_all_template():
    current_user = get_jwt_identity()  # Get the identity of the current user
    user_from_db = users_collection.find_one({'email': current_user})
    if user_from_db:
        # return an empty response
        # del user_from_db['_id'], user_from_db['password']
        # return jsonify({'profile': user_from_db}), 200
        return jsonify(''), 200
    else:
        return jsonify({'msg': 'You are not authenticated'}), 404


if __name__ == '__main__':
    app.run(debug=True)
