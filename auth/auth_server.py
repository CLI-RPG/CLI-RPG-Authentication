from pymongo import MongoClient
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

DATABASE = os.environ.get('MONGO_AUTH_DATABASE')
COLLECTION = os.environ.get('MONGO_AUTH_COLLECTION')
client = MongoClient('mongodb://mongo:27017/',
    username=os.environ.get('MONGO_AUTH_USERNAME'),
    password=os.environ.get('MONGO_AUTH_PASSWORD')
)

print("Authenthication server connected to database! :)")

db = client[DATABASE]
collection = db[COLLECTION]

@app.route("/register", methods=["POST"])
def register():
    data = request.json
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
    return res != None

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if authenticate_user(username, password):
        return Response(status=200) # TODO give token/cookie whatever
    else:
        return Response(status=401)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
