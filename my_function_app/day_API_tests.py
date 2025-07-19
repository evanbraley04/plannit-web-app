import requests
from dotenv import load_dotenv
load_dotenv()
import os

add_day_url = os.getenv("ADD_DAY_AZURE_URL")
get_day_url = os.getenv("GET_DAY_AZURE_URL")
get_days_url = os.getenv("GET_DAYS_AZURE_URL")
update_day_url = os.getenv("UPDATE_DAY_AZURE_URL")
delete_day_url = os.getenv("DELETE_DAY_AZURE_URL")
host_key = os.getenv("AZURE_FUNCTION_HOST_KEY")

def day_tests():

    res = requests.post(add_day_url, json={
        'planner_id':'1234567890',
        'day_name':'Friday',
        'event_id_list': []},
        params = {'code': host_key})
    print('checking add day:', res.status_code, res.text)
    
    the_id = res.text
    res = requests.get(get_day_url+the_id, params = {'code' : host_key})
    print('checking get day:', res.status_code, res.text)
    
    res = requests.post(add_day_url,json={
        'planner_id':'11111111',
        'day_name':'Tuesday',
        'event_id_list': ['Math Recitation', 'Breakfast with Max', 'IT Lecture ', 'Nap Time', 'Dinner with John']}, 
        params = {'code' : host_key})

    res = requests.get(get_days_url, params = {'code' : host_key})
    print('checking get days:', res.status_code, res.text) 

    res = requests.put(update_day_url+the_id,json={
        'attribute':'day_name',
        'value':'Monday'}, params = {'code' : host_key})
    print('checking update day:', res.status_code, res.text)

    res = requests.get(get_days_url, params = {'code' : host_key})
    print('checking get days after update:', res.status_code, res.text) 
    
    res = requests.delete(delete_day_url+the_id, params = {'code' : host_key})
    print('checking delete day:', res.status_code, res.text)

    res = requests.get(get_days_url, params = {'code' : host_key})
    print('checking get days after delete:', res.status_code, res.text) 

    res = requests.post(add_day_url,json={
        'planner_id':'33333333',
        'day_name':'Wednesday',
        'event_id_list': ['Take Care of Children', 'Education Class', 'Irish Class', 'Groceries with Ashton', 'Dinner with Robert']}, params = {'code' : host_key})

    res = requests.post(add_day_url,json={
        'planner_id':'13131313',
        'day_name':'Friday',
        'event_id_list': ['CS Lab', 'Work', 'Cook Dinner']}, params = {'code' : host_key})
    
if __name__=="__main__":
    day_tests()