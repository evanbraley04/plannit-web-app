import requests, json
from flask_login import UserMixin
from dotenv import load_dotenv
load_dotenv()
import os

get_user_id_url = os.getenv("GET_USER_ID_AZURE_URL")
get_user_username_url = os.getenv("GET_USER_USERNAME_AZURE_URL")

host_key = os.getenv("AZURE_FUNCTION_HOST_KEY")

# inherit from UserMixin
class User(UserMixin):

    # constructor
    def __init__(self,username,_id,active=True):
        self.username = username
        self.id = _id
        self.active = active
        self.roles = []
        if self.username == 'admin':
                self.add_role('admin')

    def add_role(self,role):
        self.roles.append(role)

    def get(user_id):
        u = get_user_by_id(user_id)
        if u:
            # construct a User object; check roles
            user = User(u.get('username'),u.get('_id'))
            
           
            return user

def authenticate( username, password ):
    # make sure that user and pass are provided
    if username != None and password != None:
        # get user by username
        result = (requests.get(get_user_username_url+username, 
            params = {'code': host_key}))
        user_dict = json.loads(result.text)
        # if password matches, return user
        if user_dict == None:
            return None
        pw = user_dict.get('password')
        if password == pw:
            return user_dict
        else:
            return None
    else:
        return None

def get_user( username ):
    # make a GET request to your user service
    result = (requests.get(get_user_username_url+username, 
        params = {'code': host_key}))
    user_dict = json.loads(result.text)
    # if user, return user
    if user_dict:
        return user_dict
    else:
        return None

def get_user_by_id( _id ):
    # make a GET request to your user service
    result = (requests.get(get_user_id_url+_id, 
        params = {'code': host_key}))
    user_dict = json.loads(result.text)
    # if user, return user
    if user_dict:
        return user_dict
    else:
        return None

# you can have other methods here.  
# having service requests in user_model helps to separate the model from control (routes).
