import requests
from dotenv import load_dotenv
load_dotenv()
import os

add_planner_url = os.getenv('ADD_PLANNER_AZURE_URL')
get_planner_url = os.getenv("GET_PLANNER_AZURE_URL") 
get_planners_url = os.getenv("GET_PLANNERS_AZURE_URL")
update_planner_url = os.getenv("UPDATE_PLANNER_AZURE_URL")
delete_planner_url = os.getenv("DELETE_PLANNER_AZURE_URL")
host_key = os.getenv("AZURE_FUNCTION_HOST_KEY")

def planner_tests():
    
    # post
    post_res = requests.post(add_planner_url, json={
            'day_id_list' : [],
            'user_id' : 'lol'
        }, params = {'code' : host_key})
    print("planner add check: ", post_res.status_code, post_res.text)
    
    test_planner_id = post_res.text
    
    # get
    get_res = requests.get(get_planner_url+test_planner_id, params = {'code' : host_key})
    print("planner get check: ", get_res.status_code, get_res.text)
    
    # put
    put_res = requests.put(update_planner_url+test_planner_id, json={
            'plannerid' : test_planner_id,
            'attr' : 'user_id',
            'value' : 'gaming'
        }, params = {'code' : host_key})
    print("planner put check: ", put_res.status_code, put_res.text)
    
    # delete
    delete_res = requests.delete(delete_planner_url+test_planner_id, params = {'code' : host_key})
    print("planner delete check: ", delete_res.status_code, delete_res.text)

planner_tests()