from pymongo import MongoClient
from pymongo.collection import Collection
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import os
import jwt
import json
import http
import typing
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)

DATABASE = os.environ.get('MONGO_AUTH_DATABASE')
if DATABASE is None:
    exit(-1)
COLLECTION = os.environ.get('MONGO_AUTH_COLLECTION')
if COLLECTION is None:
    exit(-1)
client = MongoClient('mongodb://mongo_auth:27017/',
    username=os.environ.get('MONGO_INITDB_ROOT_USERNAME'),
    password=os.environ.get('MONGO_INITDB_ROOT_PASSWORD')
)

if client is None:
    print("coluld not connect")
    exit(-1);

print("Authenthication server connected to database! :)")

db = client[DATABASE]
collection = db[COLLECTION]

@app.route("/auth/register", methods=["POST"])
def register():
    data = request.json
    if data is None:
        return Response(status=http.HTTPStatus.BAD_REQUEST)
    username = data.get('username')
    password = data.get('password')
    res = collection.find_one({'username': username})
    if res:
        return Response(status=409)
    user = {
        "username": username,
        "password": password,
        "role": False
    }
    result = collection.insert_one(user)
    return Response(status=200)

def authenticate_user(username, password):
    res = collection.find_one({'username': username, 'password': password})
    if res is None:
        return None
    print(res)
    uid = res["_id"].__str__()
    return jwt.encode({"username" : username, "user_id": uid}, "secret", algorithm="HS256")

@app.route("/auth/login", methods=["POST"])
def login():
    data = request.json
    if data is None:
        return Response(status=http.HTTPStatus.BAD_REQUEST)
    username = data.get('username')
    password = data.get('password')
    token = authenticate_user(username, password)
    if token is not None:
        return Response(status=200, response=json.dumps({'token': token})) # TODO give token/cookie whatever
    else:
        return Response(status=401)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
