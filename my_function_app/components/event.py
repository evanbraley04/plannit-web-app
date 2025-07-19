import pymongo
from bson import ObjectId
from dotenv import load_dotenv
load_dotenv()
import os
import certifi

myEvents = None

# connect to event collection in database
def connect(database_link: str):
    global myEvents
    myClient = pymongo.MongoClient(
        database_link,
        tls=True,
        tlsCAFile=certifi.where()
    )
    myDB = myClient["myDB"]
    myEvents = myDB["events"]

# deletes the user collection
def reset():
    global myEvents
    myEvents.drop()

# adds event to database, returns id
# we don't need the functionality of unique events as 
# events can appear more than once, so the functionality
# "specific" usernames for users doesn't apply
# to the event object
def add_event(title: str, time: str, day_id: str) -> str:
    global myEvents
    newEvent = {"title": title, "time": time, "day_id": day_id, "active": True}
    event = myEvents.insert_one(newEvent)
    return (str(event.inserted_id))

# returns event (dict) based on id
def get_event(_id) -> dict:
    global myEvents
    oid = ObjectId(_id)
    myQuery = {'_id': oid, 'active': True}
    for dictionary in myEvents.find(myQuery):
        dictionary['_id'] = str(oid)
        return dictionary

# returns list of events
def get_events() -> list:
    global myEvents
    eventList = []
    myQuery = {'active': True}
    for event in myEvents.find(myQuery):
        dictionary = event
        dictionary['_id'] = str(dictionary['_id'])
        eventList.append(dictionary)
    return eventList

# updates value of chosen attribute of particular id
def update_event(_id, attr, val) -> bool:
    global myEvents
    oid = ObjectId(_id)
    myQuery = {'_id': oid, 'active': True}
    myUpdate = {attr: val}
    result = myEvents.update_one(myQuery, {'$set': myUpdate})
    return result.modified_count > 0

# deletes user based on id
def delete_event( _id ) -> bool:
    global myEvents
    oid = ObjectId(_id)
    myQuery = {'_id': oid}
    myUpdate = {'active': False}
    return myEvents.update_one(myQuery, {'$set': myUpdate}).acknowledged

# unit tests
if __name__ == '__main__':
    connect(os.getenv("MONGO_URI"))
    id = add_event('CS Homework', '8:30 PM', 'Wednesday') # adding event
    print("Checking event can be added and gotten from id...")
    print(get_event(id))
    print("Checking updating event returns True")
    print("Updating event returns..." + str(update_event(id, 'title', 'Math Homework'))) # updating event
    print("Checking event was updated...")
    print(get_event(id))
    id2 = add_event('Walk The Dog', '3:45 PM', 'Thursday') # adding second event
    print("Checking another event can be added and gotten from id...")
    print(get_event(id2))
    print("Checking updating another event returns True")
    print("Updating another event returns..." + str(update_event(id2, 'time', '4:30 PM'))) # updating second event
    print("Checking another event was updated...")
    print(get_event(id2))
    print("Checking all events can be gotten...")
    print(get_events())
    #delete_event(id2) # delete event
    print("Checking events can be deleted...")
    print(get_events())
    print("Checking updating deleted event returns False")
    print("Updating deleted event returns..." + str(update_event(id2, 'time', '5:15 PM'))) # updating deleted event
    #reset()
    print("Checking that reset deletes all events...")
    print(get_events())