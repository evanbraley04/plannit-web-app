import requests
import function_app
from dotenv import load_dotenv
load_dotenv()
import os

add_event_url = os.getenv("ADD_EVENT_AZURE_URL")
get_event_url = os.getenv("GET_EVENT_AZURE_URL")
get_events_url = os.getenv("GET_EVENTS_AZURE_URL")
update_event_url = os.getenv("UPDATE_EVENT_AZURE_URL")
delete_event_url =  os.getenv("DELETE_EVENT_AZURE_URL")
delete_events_url = os.getenv("DELETE_EVENTS_AZURE_URL")
host_key = os.getenv("AZURE_FUNCTION_HOST_KEY")

def event_tests():

    res = requests.post(add_event_url, json={
        'title':'CS518 Homework',
        'time':'5:30 PM',
        'day_id':'Friday'}, params = {'code' : host_key})
    print('add event:', res.status_code, res.text)


    print('add event response:', res.status_code, res.text)
    event_id = res.text.strip()
    print('event_id:', repr(event_id))


    event_id = res.text

    res = requests.get(get_event_url + event_id, params = {'code' : host_key})
    print('get event:', res.status_code, res.text)

    res = requests.get(get_events_url, params = {'code' : host_key})
    print('get events:', res.status_code, res.text)

    res = requests.put(update_event_url + event_id, json={
        'attr': 'time',
        'val': '6:00 PM'}, params = {'code' : host_key})
    print('update event:', res.status_code, res.text)

    res = requests.delete(delete_event_url + event_id, params = {'code' : host_key})
    print('delete event:', res.status_code, res.text)

    res = requests.delete(delete_events_url, params = {'code' : host_key})
    print('delete events:', res.status_code, res.text)

    # to check if delete events worked
    res = requests.get(get_events_url, params = {'code' : host_key})
    print('get events:', res.status_code, res.text)

# run the tests
event_tests()