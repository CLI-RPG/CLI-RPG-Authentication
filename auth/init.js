db = db.getSiblingDB('auth');
db.createCollection('client');
db.client.insert({
    "id": 1,
    "username": "barbie",
    "password": "15065d771f7c8746bd30c125f9bb68a5ec7a84fccd7f0a82b38e760f39521c05",
    "role": True
});