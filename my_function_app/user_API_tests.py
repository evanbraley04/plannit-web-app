import requests
from dotenv import load_dotenv
load_dotenv()
import os

add_user_url = os.getenv("ADD_USER_AZURE_URL")
get_user_id_url = os.getenv("GET_USER_ID_AZURE_URL")
get_user_username_url = os.getenv("GET_USER_USERNAME_AZURE_URL")
get_users_url = os.getenv("GET_USERS_AZURE_URL")
update_user_url = os.getenv("UPDATE_USER_AZURE_URL")
delete_user_url = os.getenv("DELETE_USER_AZURE_URL")
host_key = os.getenv("AZURE_FUNCTION_HOST_KEY")

def user_tests():

    print(add_user_url+host_key)
    res = requests.post(add_user_url, json={
        'username':'user2',
        'password':'password1',
        'planner_id':'1234567890',
        'friends': []}, params = {'code' : host_key})
    print('add user:', res.status_code, res.text)
    
    the_id = res.text
    res = requests.get(get_user_id_url+the_id, params = {'code' : host_key})
    print('get user:', res.status_code, res.text)
    
    res = requests.post(add_user_url, json={
        'username':'user2',
        'password':'password2',
        'planner_id':'12345',
        'friends': ['user1']}, params = {'code' : host_key})
    print('add user:', res.status_code, res.text)
    
    
    
    res = requests.get(get_users_url, params = {'code' : host_key})
    print('get users:', res.status_code, res.text)

    res = requests.put(update_user_url+the_id,json={
        'attr':'username',
        'val':'user3'}, params = {'code' : host_key})
    print('update user:', res.status_code, res.text)
    
    res = requests.delete(delete_user_url+the_id, params = {'code' : host_key})
    print('delete user:', res.status_code, res.text)
    
if __name__=="__main__":
    user_tests()