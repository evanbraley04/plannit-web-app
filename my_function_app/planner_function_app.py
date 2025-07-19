import azure.functions as func
import datetime
import json
import logging
from dotenv import load_dotenv
load_dotenv()
import os
from components import planner

mongo_db = os.getenv("MONGO_URI")

from function_app import app

@app.function_name(name="add_planner")
@app.route(route="add_planner", auth_level=func.AuthLevel.FUNCTION, methods=('POST',))
def add_planner(req: func.HttpRequest) -> func.HttpResponse:

    # handle failure case...
    try:
        planner.connect(mongo_db)
        
        req_body = req.get_json()
        days_of_week = req_body.get('day_id_list')
        connected_user_id = req_body.get('user_id')
        
        # makes this of type string instead of OBid
        result = str(planner.add_planner(days_of_week, connected_user_id))
        
        # create a user with the given user id and days of week
        return func.HttpResponse(status_code=201, body=result)
    except Exception as e:
        return func.HttpResponse(status_code=409, body=str(e))


@app.function_name(name="get_planner")
@app.route(route="get_planner/{plannerid}", auth_level=func.AuthLevel.FUNCTION, methods=('GET',))
def get_planner(req: func.HttpRequest) -> func.HttpResponse:
    
    try:
        planner.connect(mongo_db)
        
        plannerid = req.route_params.get('plannerid')

        # get planner by planner_id
        return func.HttpResponse(status_code=200, body=str(planner.get_planner(plannerid)))
    except Exception as e:
        return func.HttpResponse(status_code=409, body=str(e))


@app.function_name(name="get_planners")
@app.route(route="get_planners", auth_level=func.AuthLevel.FUNCTION, methods=('GET',))
def get_planners(req: func.HttpRequest) -> func.HttpResponse:
	try:
		planner.connect(mongo_db)
		
		return func.HttpResponse(status_code=200, body=str(planner.get_planners()))
	except Exception as e:
		return func.HttpResponse(status_code=409, body=str(e))



@app.function_name(name="update_planner")
@app.route(route="update_planner/{plannerid}", auth_level=func.AuthLevel.FUNCTION, methods=('PUT',))
def update_planner(req: func.HttpRequest) -> func.HttpResponse:
    
    try:
        planner.connect(mongo_db)
        
        req_body = req.get_json()
        plannerid = req.route_params.get('plannerid')
        attr = req_body.get('attr')
        value = req_body.get('value')
        
        return func.HttpResponse(status_code=200, body=str(planner.update_planner(plannerid, attr, value)))
    except Exception as e:
        return func.HttpResponse(status_code=409, body=str(e))


@app.function_name(name="delete_planner")
@app.route(route="delete_planner/{plannerid}", auth_level=func.AuthLevel.FUNCTION, methods=('DELETE',))
def delete_planner(req: func.HttpRequest) -> func.HttpResponse:
    
    try:
        planner.connect(mongo_db)
        
        plannerid = req.route_params.get('plannerid')
        return func.HttpResponse(status_code=200, body=str(planner.delete_planner(plannerid)))
    except Exception as e:
        return func.HttpResponse(status_code=409, body=str(e))
