import pymongo
from pprint import pprint
from bson import ObjectId
from dotenv import load_dotenv
load_dotenv()
import os
import certifi

myDays = None

# connect to day collection in database
def connect(database_link : str):
    global myDays
    myClient = pymongo.MongoClient(
        database_link,
        tls=True,
        tlsCAFile=certifi.where()
    )
    myDB = myClient["myDB"]
    myDays = myDB["days"]

# deletes day collection
def reset():
    global myDays
    myDays.drop()

# adds day to database, returns id
def add_day(day_name: str, event_id_list: list, planner_id: str) -> str:
    global myDays
    day_data = {
        "day_name":day_name, 
        "event_id_list":event_id_list, 
        "planner_id":planner_id, 
        "active":True}
    day = myDays.insert_one(day_data)
    return (str(day.inserted_id))

# returns day (dict) based on id
def get_day(_id) -> dict:
    global myDays
    obID = ObjectId(_id)
    myQuery = {'_id':obID, 'active':True}
    dict = myDays.find_one(myQuery)
    if type(dict) != type(None):
        dict['_id'] = str(dict['_id'])
    return dict
    
# returns list of days
def get_days() ->list:
    global myDays
    day_list = []
    for day in myDays.find({'active':True}):
        dict = day
        dict['_id'] = str(dict['_id'])
        day_list.append(dict)
    return day_list

# updates value of chosen attribute of particular id
def update_day(_id, attribute, value) -> bool:
    global myDays
    obID = ObjectId(_id)
    myQuery = {'_id': obID, 'active':True}
    dict = myDays.find_one(myQuery)
    if type(dict) != type(None):
        myUpdate = {attribute: value}
        return (myDays.update_one(myQuery, {'$set': myUpdate})).acknowledged 
    else:
        return False

# deletes day based on id
def delete_day(_id) -> bool:
    global myDays
    obID = ObjectId(_id)
    myQuery = {'_id': obID, 'active':True}
    myDelete = {'active': False}
    return (myDays.update_one(myQuery, {'$set': myDelete})).acknowledged

# unit tests
if __name__ == '__main__':
    connect(os.getenv("MONGO_URI"))
    reset()
    print("Checking if a day can be added and the id can be retrieved...")
    id1 = add_day('Friday', ['Study Sesh', 'CS Lab', 'Zumba', 'Dinner with Mom'], "Planner") # adding day
    print(get_day(id1), "\n")
    print("Checking if day_name can be updated...")
    update_day(id1, 'day_name', 'Wednesday') # updating day
    print(get_day(id1), "\n")
    id2 = add_day('Sunday', ['Brunch with friends', 'Cleaning', 'Movie Night!'], "Planner") # adding another day
    print("Checking if event_id_list can be updated...")
    update_day(id2, 'event_id_list', ['Brunch with friends', 'Movie Night!']) # updating second day
    print(get_day(id2), "\n")
    print("Checking if list of days can be retrived...")
    print(get_days(), "\n")
    print("Checking if get_days returns all days")
    print(get_days(), "\n")
    print("Checking if day can be deleted...")
    delete_day(id1) # deleting day
    print("Checking if get_days shows the deleted day...")
    print(get_days(), "\n")
    print("Checking if a deleted day can be gotten...")
    print(get_day(id1), "\n")
    print("Checking if deleted day can be updated...")
    print(update_day(id1, 'day_name', 'Monday'), "\n")
    print("Checking if reset deletes all days...")
    reset()
    print(get_days())

