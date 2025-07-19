import pymongo
from bson import ObjectId
from dotenv import load_dotenv
load_dotenv()
import os
import certifi

global myPlanners

def connect(database_link : str):
  global myPlanners
  myClient = pymongo.MongoClient(
      database_link,
      tls=True,
      tlsCAFile=certifi.where()
  )
  myDB = myClient["myDB"]
  myPlanners = myDB["planners"]

def reset():
  global myPlanners
  myPlanners.drop()

def add_planner(day_id_list : list, user_id : str) -> str:
  global myPlanners
  planner = {
    "active" : True,
    "day_id_list" : day_id_list,
    "user_id" : user_id
  }
  return str(myPlanners.insert_one(planner).inserted_id)

def get_planner(planner_id : str) -> dict:
  global myPlanners
  return myPlanners.find_one({"_id" : ObjectId(planner_id), "active" : True})

def get_planners() -> list:
  global myPlanners
  return list(myPlanners.find({"active" : True}))

def update_planner(planner_id : str, attr : str, value) -> bool:
  global myPlanners
  return (myPlanners.update_one({"_id" : ObjectId(planner_id), "active" : True}, {"$set" : {attr : value}})).acknowledged

def delete_planner(planner_id : str) -> bool:
  global myPlanners
  return (myPlanners.update_one({"_id" : ObjectId(planner_id)}, {"$set" : {"active" : False}})).acknowledged

def get_user(planner_id : str) -> str:
  return get_planner(planner_id)["user_id"]

def get_day_id_list(planner_id : str) -> list:
  return get_planner(planner_id)["day_id_list"]

if __name__ == "__main__":
  connect(os.getenv("MONGO_URI"))
  reset() # ensure database has been cleared for tests
  planner1 = add_planner(["event collection A1", "event collection A2"], "user_id day")
  print("Check that planner has been added to database")
  print(planner1)
  print(get_planner(planner1))
  planner2 = add_planner(["event collection B1", "event collection B2"], "user_id day") # create a second planner
  print("Check that bother planners are added to the database")
  print(get_planners())
  print("Test that the user_id field can be changed")
  print(update_planner(planner1, "user_id", "lunar day?")) # test that the user_id field can be changed
  print("Verify that the field was indeed changed")
  print(get_planners())
  print("Test that we can delete planner1")
  print(delete_planner(planner1))
  print("Test that planner1 was deleted")
  print(get_planner(planner1))
  print("Test that planner1 cannot be updated")
  print(update_planner(planner1, "user_id", "123487923147r42"))
  print("Test that planner2 was unchanged")
  print(get_planner(planner2))
  print("Test that getting all planners doesn't show deleted ones")
  print(get_planners())
  print("Test get_day_id_list() function")
  print(get_day_id_list(planner2))
