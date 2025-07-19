import azure.functions as func
import datetime
import json
import logging
from components import day
from dotenv import load_dotenv
load_dotenv()
import os

from function_app import app

@app.function_name(name="add_day")
@app.route(route="add_day", auth_level=func.AuthLevel.FUNCTION, methods=('POST',))
def add_day(req: func.HttpRequest) -> func.HttpResponse:

    req_body = req.get_json()
    planner_id = req_body.get('planner_id')
    day_name = req_body.get('day_name')
    event_id_list = req_body.get('event_id_list')
    
    # create a day with the given planner_id, day_name, event_id_list (empty for now until updated)
    day.connect(os.getenv("MONGO_URI"))
    result = str(day.add_day(day_name, event_id_list, planner_id))
    
    # return an appropriate response       
    return func.HttpResponse(status_code=201, body=result)


@app.function_name(name="get_day")
@app.route(route="get_day/{id}", auth_level=func.AuthLevel.FUNCTION, methods=('GET',))
def get_day(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    _id = req.route_params.get('id')

    # get day by id
    day.connect(os.getenv("MONGO_URI"))
    result = (day.get_day(_id))
    json_data = json.dumps(result)
    
    # return an appropriate response
    return func.HttpResponse(status_code=200, body=json_data)


@app.function_name(name="get_days")
@app.route(route="get_days/", auth_level=func.AuthLevel.FUNCTION, methods=('GET',))
def get_days(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    day.connect(os.getenv("MONGO_URI"))
    result = json.dumps(day.get_days())
    
    # return an appropriate response
    return func.HttpResponse(status_code=200, body=result)


@app.function_name(name="update_day")
@app.route(route="update_day/{id}", auth_level=func.AuthLevel.FUNCTION, methods=('PUT',))
def update_day(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    req_body = req.get_json()
    _id = req.route_params.get('id')
    logging.info("_id is:" + _id)
    attribute = req_body.get('attribute')
    value = req_body.get('value')

    # update day by id
    day.connect(os.getenv("MONGO_URI"))
    result = str(day.update_day(_id, attribute, value))
    
    # return an appropriate response
    return func.HttpResponse(status_code=200, body=result)


@app.function_name(name="delete_day")
@app.route(route="delete_day/{id}", auth_level=func.AuthLevel.FUNCTION, methods=('DELETE',))
def delete_day(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    _id = req.route_params.get('id')

    # delete day by id
    day.connect(os.getenv("MONGO_URI"))
    day.delete_day(_id)
    
    # return an appropriate response
    return func.HttpResponse(status_code=200, body="success!")