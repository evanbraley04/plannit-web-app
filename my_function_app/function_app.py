import azure.functions as func
from azure.functions import FunctionApp

app = FunctionApp()

import day_function_app
import event_function_app
import planner_function_app
import user_function_app

# from day_function_app import add_day, get_day, get_days, update_day, delete_day
# from event_function_app import add_event, get_event, get_events, update_event, delete_event, delete events
# from planner_function_app import add_planner, get_planner, get_planners, update_planner, delete_planner
# from user_function_app import add_user, get_user_id, get_user_username, get_users, update_user, delete_user