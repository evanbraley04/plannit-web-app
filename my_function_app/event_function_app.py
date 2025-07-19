import azure.functions as func
import datetime
import json
import logging
from components import event
from dotenv import load_dotenv
load_dotenv()
import os

from function_app import app

@app.function_name(name="add_event")
@app.route(route="add_event/", auth_level=func.AuthLevel.FUNCTION, methods=('POST', ))
def add_event(req: func.HttpRequest) -> func.HttpResponse:
    
    req_body = req.get_json()
    title = req_body.get('title')
    time = req_body.get('time')
    day_id = req_body.get('day_id')

    event.connect(os.getenv("MONGO_URI"))
    event_id = str(event.add_event(title, time, day_id))
    
    return func.HttpResponse(status_code=201, body=event_id)


@app.function_name(name="get_event")
@app.route(route="get_event/{id}", auth_level=func.AuthLevel.FUNCTION, methods=('GET',))
def get_event(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    _id = req.route_params.get('id')

    event.connect(os.getenv("MONGO_URI"))
    result = event.get_event(_id)

    json_data = json.dumps(result)

    return func.HttpResponse(status_code=200, body=json_data)


@app.function_name(name="get_events")
@app.route(route="get_events/", auth_level=func.AuthLevel.FUNCTION, methods=('GET',))
def get_events(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    event.connect(os.getenv("MONGO_URI"))
    result = event.get_events()

    json_data = json.dumps(result)

    return func.HttpResponse(status_code=200, body=json_data)


@app.function_name(name="update_event")
@app.route(route="update_event/{id}", auth_level=func.AuthLevel.FUNCTION, methods=('PUT',))
def update_event(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    _id = req.route_params.get('id')
    logging.info("_id is:" + _id)
    attr = req_body.get('attr')
    val = req_body.get('val')

    event.connect(os.getenv("MONGO_URI"))
    event.update_event(_id, attr, val)
    result = str(event.get_event(_id))
    return func.HttpResponse(status_code=200, body=result)


@app.function_name(name="delete_event")
@app.route(route="delete_event/{id}", auth_level=func.AuthLevel.FUNCTION, methods=('DELETE',))
def delete_event(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    _id = req.route_params.get('id')

    event.connect(os.getenv("MONGO_URI"))
    event.delete_event(_id)
    return func.HttpResponse(status_code=200, body='success!')


@app.function_name(name="delete_events")
@app.route(route="delete_events/", auth_level=func.AuthLevel.FUNCTION, methods=('DELETE',))
def delete_events(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    event.connect(os.getenv("MONGO_URI"))
    event.reset()
    return func.HttpResponse(status_code=200, body='success!')    