import hashlib
from flask import Flask, make_response, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from bson import ObjectId

from api import app, users_collection, template_collection


@app.route("/register", methods=["POST"])
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


@app.route("/login", methods=["POST"])
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


@app.route("/templates", methods=["GET", "POST"])
@jwt_required()
def get_all_template():
    if request.method == 'GET':
        templates = []
        for template in template_collection.find():
            template["_id"] = str(template["_id"])
            templates.append(template)
        return make_response(jsonify(templates)) 

    elif request.method == 'POST':
        template = request.get_json()
        template_collection.insert_one(template)
        return make_response("", 201)


@app.route("/templates/<template_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def get_single_template(template_id):
    # get a single record
    if request.method == 'GET': 
        try:
            template = template_collection.find_one({"_id": ObjectId(template_id)})
            template["_id"] = str(template["_id"])
            return make_response(jsonify(template))
        except:
            # Object with id not found
            return make_response({'msg': 'Not found'}, 404)
    
    # update a record
    elif request.method == 'PUT':
        try:
            template_collection.find_one_and_update({"_id": ObjectId(template_id)}, {"$set": request.get_json()})
            return make_response("", 200)
        except:
            # Object with id not found
            return make_response({'msg': 'not found'}, 404)
        
    # delete a single record
    elif request.method == 'DELETE': 
        try:
            template = template_collection.find_one_and_delete({"_id": ObjectId(template_id)})
            return make_response("", 200)
        except:
            # Object with id not found
            return make_response({'msg': 'Not found'}, 404)
