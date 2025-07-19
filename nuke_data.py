# nuke_data.py
# clears all databases completely
from dotenv import load_dotenv
load_dotenv()
import os
import pymongo

# demolish days
myDaysClient = pymongo.MongoClient(os.getenv("MONGO_URI"))
myDaysDB = myDaysClient["myDB"]
myDays = myDaysDB["days"]
myDays.drop()

# explode events
myEventsClient = pymongo.MongoClient(os.getenv("MONGO_URI"))
myEventsDB = myEventsClient["myDB"]
myEvents = myEventsDB["events"]
myEvents.drop()

# purge planners
myPlannersClient = pymongo.MongoClient(os.getenv("MONGO_URI"))
myPlannersDB = myPlannersClient["myDB"]
myPlanners = myPlannersDB["planners"]
myPlanners.drop()

# un-make users
myUsersClient = pymongo.MongoClient(os.getenv("MONGO_URI"))
myUsersDB = myUsersClient["myDB"]
myUsers = myUsersDB['users']
myUsers.drop()