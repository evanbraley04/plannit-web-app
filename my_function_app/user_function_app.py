import azure.functions as func
import datetime
import json
import logging
from components import users
from dotenv import load_dotenv
load_dotenv()
import os

from function_app import app

@app.function_name(name="add_user")
@app.route(route="add_user", auth_level=func.AuthLevel.FUNCTION, methods=('POST',))
def add_user(req: func.HttpRequest) -> func.HttpResponse:

    try:
        req_body = req.get_json()
        username = req_body.get('username')
        password = req_body.get('password')
        planner_id = req_body.get('planner_id')
        friends = req_body.get('friends')
        
        # create a user with the given planner_id, username, password and friends (empty for now until updated)
        users.connect(os.getenv("MONGO_URI"))
        result = str(users.add_user(username, password, planner_id, friends))
        
        # return an appropriate response       
        return func.HttpResponse(status_code=201, body=result)
    except Exception as e:
        return func.HttpResponse(status_code=409, body=str(e))


@app.function_name(name="get_user_id")
@app.route(route="get_user_id/{id}", auth_level=func.AuthLevel.FUNCTION, methods=('GET',))
def get_user_id(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        _id = req.route_params.get('id')

        # get user by id
        # _id = _id[4:]
        users.connect(os.getenv("MONGO_URI"))
        result = (users.get_user_id(_id))
        
        json_data = json.dumps(result)
        
        # return an appropriate response
        return func.HttpResponse(status_code=200, body=json_data)
    except Exception as e:
        return func.HttpResponse(status_code=409, body=str(e))
    

@app.function_name(name="get_user_username")
@app.route(route="get_user_username/{username}", auth_level=func.AuthLevel.FUNCTION, methods=('GET',))
def get_user_username(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        username = req.route_params.get('username')

        # get user by username
        users.connect(os.getenv("MONGO_URI"))
        result = (users.get_user_username(username))
        
        json_data = json.dumps(result)
        
        # return an appropriate response
        return func.HttpResponse(status_code=200, body=json_data)
    except Exception as e:
        return func.HttpResponse(status_code=409, body=str(e))    
    


@app.function_name(name="get_users")
@app.route(route="get_users/", auth_level=func.AuthLevel.FUNCTION, methods=('GET',))
def get_users(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        users.connect(os.getenv("MONGO_URI"))
        result = json.dumps(users.get_users())
        
        # return an appropriate response
        return func.HttpResponse(status_code=200, body=result)
    except Exception as e:
        return func.HttpResponse(status_code=409, body=str(e))


@app.function_name(name="update_user")
@app.route(route="update_user/{id}", auth_level=func.AuthLevel.FUNCTION, methods=('PUT',))
def update_user(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        req_body = req.get_json()
        _id = req.route_params.get('id')
        
        attr = req_body.get('attr')
        val = req_body.get('val')

        # update user by id
        # _id = _id[4:]
        users.connect(os.getenv("MONGO_URI"))
        result = str(users.update_user(_id, attr, val))
    except Exception as e:
        return func.HttpResponse(status_code=409, body=str(e))
    
    # return an appropriate response
    return func.HttpResponse(status_code=200, body=result)


@app.function_name(name="delete_user")
@app.route(route="delete_user/{id}", auth_level=func.AuthLevel.FUNCTION, methods=('DELETE',))
def delete_user(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    #_id = req.route_params.get('username')
    _id = req.route_params.get('id')

    # delete user by id
    # _id = _id[4:]
    users.connect(os.getenv("MONGO_URI"))
        
    result = str(users.delete_user(_id))
    # return an appropriate response
    return func.HttpResponse(status_code=200, body=result)
    
    
# @app.route(route="signup_user/", auth_level=func.AuthLevel.FUNCTION, methods=('POST', 'GET'))
# def signup_user(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')
    
#     req_body = req.get_json()
#     username = req_body.get('username')
#     password = req_body.get('password')
    
#     # create a user with the given planner_id, username, password and friends (empty for now until updated)
#     users.connect(os.getenv("MONGO_URI"))
#     result = str(users.add_user(username, password))   
    
#     return func.HttpResponse(status_code=201, body=result)