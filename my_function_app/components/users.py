import pymongo
from pprint import pprint
from bson import ObjectId
from dotenv import load_dotenv
load_dotenv()
import os
import certifi

global myUsers
global user_data
myUsers = None

def connect(database_link: str):
    global myUsers
    myClient = pymongo.MongoClient(
        database_link,
        tls=True,
        tlsCAFile=certifi.where()
    )
    myDB = myClient["myDB"]
    myUsers = myDB['users']

def reset():
    global myUsers
    myUsers.drop()

def add_user(username: str, password: str, planner_id=0, friends=None) -> str:
    global myUsers
    global user_data
    
    result = myUsers.find_one({"username":username, "active":True})
    
    if result == None: 
        user_data = {
            "username":username,
            "password":password,
            "planner_id":planner_id,
            "friends":friends,
            "active":True
        }
        user = myUsers.insert_one(user_data)
        return(str(user.inserted_id))
    else:
        return(-1)

def get_user_id(_id) -> dict:
    global myUsers
    oid = ObjectId(_id)

    myQuery = {'_id': oid,'active':True}
    dict = myUsers.find_one(myQuery)
    if type(dict) != type(None):
        dict['_id'] = str(dict["_id"])
    return dict

def get_user_username(username) -> dict:
    global myUsers

    myQuery = {'username': username,'active':True}
    dict = myUsers.find_one(myQuery)
    if type(dict) != type(None):
        dict['_id'] = str(dict["_id"])
    return dict
  
def get_users() -> list:
    global myUsers
    userList = []
    for user in myUsers.find({'active':True}):
        dictionary = user
        dictionary['_id'] = str(dictionary['_id'])
        userList.append(dictionary)
    return userList    

def update_user(_id, attr, val):
    global myUsers
    oid = ObjectId(_id)
    myQuery = {'_id': oid,'active':True}
    dict = myUsers.find_one(myQuery)
    if type(dict) != type(None):
        myUpdate = {attr: val}
        return(myUsers.update_one(myQuery, {'$set': myUpdate})).acknowledged
    else:
        return False

def delete_user(_id: str):
    global myUsers
    global user_data
    oid = ObjectId(_id)
    myQuery = {'_id': oid,'active':True}
    myDelete = {'active':False}
    return myUsers.update_one(myQuery, {'$set': myDelete}).acknowledged


if __name__=="__main__":
    connect(os.getenv("MONGO_URI"))
    reset()
    
    print("Checking if a user can be added and ID can be created...")
    id = add_user('username1', 'password1', 'planner_id', [])
    print(get_user_id(id))
    
    print("Testing if another user can be created with same username as first user...should print 'TRUE' if username cannot be created")
    id_test = add_user('username1', 'passwordtest', 'planner_id', [])
    print(id_test == -1)
    
    print("Checking if another user can be created with the first user as a friend...")
    id2 = add_user('username2', 'password2', 'planner_id', [id])
    print(get_user_id(id2))
    
    print("Creating a third user...")
    id3 = add_user('username3', 'password3', 'planner_id', [id, id2])
    print(get_user_id(id3))
    
    print("Creating a fourth user and checking if they can hold multiple friends...")
    id4 = add_user('username4', 'password4', 'planner_id', [id, id2, id3])
    print(get_user_id(id4))
    
    print("Checking that user 1 can be updated with new friends after their creation...")
    update_user(id, 'friends', [id2, id3])
    print(get_user_id(id))
    
    print("Checking if all users can be retrieved as a list...")
    print(get_users())
    
    print("Checking if user id2 can be deleted...")
    delete_user(id2)
    print(get_users())
    
    print("Checking if deleted user can be gotten...")
    print(get_user_id(id2))
    
    print("Checking if deleted user can be updated...")
    print(update_user(id2, "password", "passwordtest2"))
    
    print("Checking list of all users after user had been deleted...")
    print(get_users())
    
    reset()
    
    print("Checking list of all users after reset()...")
    print(get_users())