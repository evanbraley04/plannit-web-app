import flask as fl
from flask import request, flash
from flask_login import login_user, logout_user, login_required, current_user
import requests, json
from bson import ObjectId
from dotenv import load_dotenv
load_dotenv()
import os

get_day_url = os.getenv("GET_DAY_AZURE_URL")
update_day_url = os.getenv("UPDATE_DAY_AZURE_URL")

add_event_url = os.getenv("ADD_EVENT_AZURE_URL")
get_event_url = os.getenv("GET_EVENT_AZURE_URL")
get_events_url = os.getenv("GET_EVENTS_AZURE_URL")
update_event_url = os.getenv("UPDATE_EVENT_AZURE_URL")
delete_event_url =  os.getenv("DELETE_EVENT_AZURE_URL")
delete_events_url = os.getenv("DELETE_EVENTS_AZURE_URL")

get_planner_url = os.getenv("GET_PLANNER_AZURE_URL") 
get_planners_url = os.getenv("GET_PLANNERS_AZURE_URL")

host_key = os.getenv("AZURE_FUNCTION_HOST_KEY") 

event_routes = fl.Blueprint('event_routes', __name__, template_folder='templates')

@event_routes.route('/event_list', defaults={'event_list': None})
@login_required
def event_list(event_list=None):
    event_list = []
    res = requests.get(get_events_url, 
        params = {'code' : host_key})
    for event in res.json():
        _id = event.get('_id')
        title = event.get('title')
        event_list.append({'_id': _id, 'title':title})
    return fl.render_template('event_list.html', event_list=event_list)



@event_routes.route("/event_data/<event_id>", methods=["GET"])    
@login_required
def event_data(event_id):
    u_id = current_user.id
    res = requests.get(get_event_url + event_id, 
        params = {'code' : host_key})
    event_data = json.loads(res.text.replace("'", '"'))
    day_id = event_data.get('day_id')
    get_day_res = requests.get(get_day_url + day_id, 
        params = {'code': host_key})
    day_dict = json.loads(get_day_res.text)
    day_name = day_dict.get('day_name')
    if 'admin' in current_user.roles:
        return fl.render_template('admin_event_data.html', event_data=event_data, event_id=event_id, day_name=day_name)
    else:
        return fl.render_template('event_data.html', share_planner_url=fl.url_for('user_routes.share_planner', id=u_id), 
                friends_planner_url=fl.url_for('user_routes.friends_planner'), create_event_url=fl.url_for('event_routes.create_event'),
                event_data=event_data, event_id=event_id, day_name=day_name)



@event_routes.route('/create_event', methods=['POST','GET'])
@login_required
def create_event():
    if (request.method == 'POST'):
        title = request.form['title']
        time = request.form['time']
        day = request.form['day']
        
        if title == '' or time == '' or day == '':
            flash("Creation Failed! Empty Fields Received")
        elif day != "Sunday" and day != "Monday" and day != "Tuesday" and day != "Wednesday" and day != "Thursday" and day != "Friday" and day != "Saturday":
            flash("Creation Failed! Invalid Day Name")
        else:
            u_id = current_user.id
            get_planners_res = requests.get(get_planners_url, 
                params = {'code' : host_key})
            matched = ""
            for planner in eval(get_planners_res.text.replace("'", '"')):
                if u_id == planner["user_id"]:
                    matched = planner["_id"]
                    break

            get_single_planner_res = requests.get(get_planner_url + str(matched), 
                params = {'code': host_key})                  
            single_planner = eval(get_single_planner_res.text)

            day_id_list = single_planner['day_id_list']

            events_day_id = ''
            day_dict = {}

            for day_id in day_id_list:
                get_day_res = requests.get(get_day_url + day_id, 
                    params = {'code': host_key})
                day_dict = json.loads(get_day_res.text)
                if day == day_dict.get('day_name'):
                    events_day_id = day_id
                    break

            response = requests.post(add_event_url, json = {
                'title': title,
                'day_id': events_day_id,
                'time': time}, 
                params={'code': host_key})

            if (response.status_code == 201):
                flash("Successfully Created Event!")
            else: 
                flash("Creation Failed!")

            day_event_id_list = day_dict.get('event_id_list')
            day_event_id_list.append(response.text)

            requests.put(update_day_url + day_id, json = {
                'attribute': 'event_id_list',
                'value': day_event_id_list
                },
                params={'code': host_key})
    if 'admin' in current_user.roles:
        return fl.render_template('admin_create_event.html')
    else:
        return fl.render_template('create_event.html', friends_planner_url=fl.url_for('user_routes.friends_planner'), share_planner_url=fl.url_for('user_routes.share_planner', id = current_user.id))



@event_routes.route('/update_event/<event_id>', methods=['POST','GET'])
@login_required
def update_event(event_id):
    u_id = current_user.id
    res = requests.get(get_event_url + event_id, 
        params = {'code' : host_key})
    event_data = json.loads(res.text.replace("'", '"'))
    event_day_id = event_data.get('day_id')
    get_day_res = requests.get(get_day_url + event_day_id, 
        params = {'code': host_key})
    day_json = json.loads(get_day_res.text)
    day_name = day_json.get('day_name')
    print("update event triggered")
    if (request.method == 'POST'):
        print("what")
        title = request.form['title']
        time = request.form['time']
        day = request.form['day']

        print("in post")

        if title != '':
            print("in title")
            response = requests.put(update_event_url + event_id, json = {
                'attr': 'title',
                'val': title}, 
                params = {'code': host_key})

            print("sent title")
        if time != '':
            response = requests.put(update_event_url + event_id, json = {
                'attr': 'time',
                'val': time}, 
                params = {'code': host_key})

            print("sent time")    
        if day != '':
            u_id = current_user.id
            get_planners_res = requests.get(get_planners_url, 
                params = {'code': host_key})
            matched = ""
            for planner in eval(get_planners_res.text.replace("'", '"')):
                if u_id == planner["user_id"]:
                    matched = planner["_id"]
                    break

            get_single_planner_res = requests.get(get_planner_url + str(matched), 
                params = {'code': host_key})                  
            single_planner = eval(get_single_planner_res.text)

            day_id_list = single_planner['day_id_list']

            events_day_id = ''
            events_day_event_list = []
            day_dict = {}
            prev_day_event_list = []
            prev_day_id = ''

            for day_id in day_id_list:
                get_day_res = requests.get(get_day_url + day_id, 
                    params = {'code': host_key})
                day_dict = json.loads(get_day_res.text)
                if day == day_dict.get('day_name'):
                    events_day_event_list = day_dict['event_id_list']
                    events_day_id = day_id
                elif event_id in day_dict['event_id_list']:
                   prev_day_event_list = day_dict['event_id_list']
                   prev_day_id = day_id

            if events_day_id != '' and prev_day_event_list != []:
                response = requests.put(update_event_url + event_id, json = {
                    'attr': 'day_id',
                    'val': events_day_id}, 
                    params = {'code': host_key})

                events_day_event_list.append(event_id)
                fernando_resp = requests.put(update_day_url + events_day_id, json = {
                    'attribute': 'event_id_list', 
                    'value': events_day_event_list}, 
                    params = {'code': host_key})
                    
                # need to update the day that has the event before it was changed
                prev_day_event_list.remove(event_id)
                julio_resp = requests.put(update_day_url + prev_day_id, json = {
                    'attribute': 'event_id_list', 
                    'value': prev_day_event_list}, 
                    params = {'code': host_key})
                flash("Successfully Updated Event!")
            else:
                flash("Update Failed!")
    
    res = requests.get(get_event_url + event_id, 
        params = {'code' : host_key})
    event_data = json.loads(res.text.replace("'", '"'))
    if 'admin' in current_user.roles:
        return fl.render_template('admin_update_event.html', event_id=event_id, event_data=event_data)
    else:
        return fl.render_template('update_event.html', share_planner_url=fl.url_for('user_routes.share_planner', id=u_id), 
                friends_planner_url=fl.url_for('user_routes.friends_planner'), create_event_url=fl.url_for('event_routes.create_event'), 
                event_id=event_id, event_data=event_data, day_name=day_name)



@event_routes.route('/delete_event/<event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    text = request.form.get('delete_input')

    if text == "delete":
        event_response = requests.get(get_event_url + event_id, 
            params = {'code' : host_key})
        event_data = json.loads(event_response.text)
        day_id = event_data['day_id']
        day_response = requests.get(get_day_url + day_id,
            params={'code' : host_key})
        day_data = json.loads(day_response.text)
        day_events_list = day_data['event_id_list']
        day_events_list.remove(event_data['_id'])
        requests.put(update_day_url + day_id, json = {
            'attribute':'event_id_list', 
            'value':day_events_list}, 
            params={'code' : host_key})

        response = requests.delete(delete_event_url + event_id, 
            params = {'code' : host_key})

        if (response.status_code == 200):
            flash("Successfully Deleted Event!")
        else:
            flash("Delete Failed!")
    
        return fl.redirect(fl.url_for('user_routes.home'))
    else:
        flash("Delete Failed! Incorrect Text Received")
        return fl.redirect(fl.url_for('event_routes.event_data', event_id=event_id))
