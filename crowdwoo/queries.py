from pymongo import Connection, DESCENDING
from bson.objectid import ObjectId

db = Connection()['crowdwoo']

# user queries

def create_user(user):
    if not bool(db.users.find({'twitter_id': user['user_id']}).count()):
        return db.users.insert({'twitter_id': user['user_id'], 'twitter_handle': user['screen_name']})

def find_user(id):
    return db.users.find_one({ '_id': ObjectId(id) })

def find_twitter_id(twitter_id):
    return db.users.find_one({ 'twitter_id': twitter_id })

def set_tokens(user, resp):
    return db.users.update({ '_id': user['_id'] }, { '$set': { 'oauth_token': resp['oauth_token'], 'oauth_token_secret': resp['oauth_token_secret'] } })

def all_users():
    return list(db.users.find())

# stats queries

def users_count():
    return db.users.find().count()