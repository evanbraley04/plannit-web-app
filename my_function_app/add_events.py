# data service test for event.py
import requests
import function_app
from dotenv import load_dotenv
load_dotenv()
import os

event_url = os.getenv("ADD_EVENT_AZURE_URL")
host_key = os.getenv("AZURE_FUNCTION_HOST_KEY")

# adding events for webapp test
res = requests.post(event_url,json={
    'title':'CS 520 Homework',
    'time':'6:30 PM',
    'day_id':'Tuesday'}, params = {'code' : host_key})
res = requests.post(event_url,json={
    'title':'Walk the Dog',
    'time':'4:20 PM',
    'day_id':'Wednesday'}, params = {'code' : host_key})
res = requests.post(event_url,json={
    'title':'CS 518 Homework',
    'time':'5:30 PM',
    'day_id':'Friday'}, params = {'code' : host_key})
res = requests.post(event_url,json={
    'title':'Dinner with Carl',
    'time':'8:30 PM',
    'day_id':'Saturday'}, params = {'code' : host_key})