# Group Testing
from dotenv import load_dotenv
load_dotenv()
import os

from user_service.components import users
import event
import day
from Planner_Service.components import planner

import pymongo
from pprint import pprint
from bson import ObjectId

event.connect(os.getenv("MONGO_URI"))
users.connect(os.getenv("MONGO_URI"))
day.connect(os.getenv("MONGO_URI"))
planner.connect(os.getenv("MONGO_URI"))

# test
bob = users.add_user("", "bob_7", "crackers24", []) # create new user
steve = users.add_user("", "steve_38", "dogs", [bob])  # create another user
users.update_user(bob, "friends", [steve]) # add friend
print("Checking user can hold another user...")
print(users.get_user(bob)) # check user can hold another user
days = [day.add_day('Sunday', [], ""), day.add_day('Monday', [], ""),
    day.add_day('Tuesday', [], ""), day.add_day('Wednesday', [], ""), 
    day.add_day('Thursday', [], ""), day.add_day('Friday', [], ""), 
    day.add_day('Saturday', [], "")]
newPlanner = planner.add_planner(days, bob)  # create planner for associated user with day objects
print("Checking planner can hold a user and day objects..")
print(planner.get_planner(newPlanner))
for oneday in days: # add planner object to each day
    day.update_day(oneday, "planner_id", newPlanner)
print("Checking day can hold a planner object...")
print(day.get_day(days[1])) # check day holds planner object
users.update_user(bob, "planner_id", newPlanner) # add planner to user
print("Checking user can hold a planner object...")
print(users.get_user(bob)) # check that planner is added
newEvent = event.add_event("doing work", '12:17 PM', days[1])  # create event with day object
print("Checking event can hold a day object...")
print(event.get_event(newEvent)) # check that event holds day object
day.update_day(days[1], "event_id_list", [newEvent]) # add event to day object
print("Checking day can hold an event object...")
print(day.get_day(days[1])) # make sure day object holds event


