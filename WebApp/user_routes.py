import flask as fl
import requests, json
from flask_login import login_user, logout_user, login_required, current_user
import user_model
from flask import Flask, flash, redirect, render_template, \
     request, url_for
from bson import ObjectId
from dotenv import load_dotenv
load_dotenv()
import os

user_routes = Flask(__name__, static_url_path='/static')

add_day_url = os.getenv("ADD_DAY_AZURE_URL")
get_day_url = os.getenv("GET_DAY_AZURE_URL")
delete_day_url = os.getenv("DELETE_DAY_AZURE_URL")

get_event_url = os.getenv("GET_EVENT_AZURE_URL")
delete_event_url =  os.getenv("DELETE_EVENT_AZURE_URL")

add_planner_url = os.getenv('ADD_PLANNER_AZURE_URL')
get_planner_url = os.getenv("GET_PLANNER_AZURE_URL") 
get_planners_url = os.getenv("GET_PLANNERS_AZURE_URL")
update_planner_url = os.getenv("UPDATE_PLANNER_AZURE_URL")
delete_planner_url = os.getenv("DELETE_PLANNER_AZURE_URL")

add_user_url = os.getenv("ADD_USER_AZURE_URL")
get_user_id_url = os.getenv("GET_USER_ID_AZURE_URL")
get_user_username_url = os.getenv("GET_USER_USERNAME_AZURE_URL")
get_users_url = os.getenv("GET_USERS_AZURE_URL")
update_user_url = os.getenv("UPDATE_USER_AZURE_URL")
delete_user_url = os.getenv("DELETE_USER_AZURE_URL")

host_key = os.getenv("AZURE_FUNCTION_HOST_KEY")

user_routes = fl.Blueprint('user_routes', __name__, template_folder='templates', static_url_path='/static')

@user_routes.route('/login',methods=['GET','POST'])
def login():
    if fl.request.method=='GET':
        return fl.render_template('index.html', signup_url = fl.url_for('user_routes.signup'))
   
    # TODO: get un and pw from form 
    
    un = request.form["username"] 
    pw = request.form["password"]

    u = user_model.authenticate(un, pw)

    if u:
        u_id = u.get('_id')
        user = user_model.User(u.get('username'),u_id)
        login_user(user)
        
        # redirect to home
        return fl.redirect(fl.url_for('user_routes.home'))

    else:
        fl.flash('Incorrect Username or Password')
        return fl.redirect(fl.url_for('user_routes.login'))

@user_routes.route('/home', methods=['GET'])
@login_required
def home():
    if 'admin' in current_user.roles:        
        return fl.render_template('admin.html', user_list_url=fl.url_for('user_routes.user_list'), create_user_url=fl.url_for('user_routes.signup'),
        day_list_url=fl.url_for('day_routes.day_list'), create_day_url=fl.url_for('day_routes.create_day'), 
        event_list_url=fl.url_for('event_routes.event_list'), create_event_url=fl.url_for('event_routes.create_event'), 
        planner_list_url=fl.url_for('planner_routes.planner'), create_planner_url=fl.url_for('planner_routes.create_planner'), 
        logout_url=fl.url_for('user_routes.logout'), current_user = current_user)
    else:
        u_id = current_user.id

        # get user's planner to get list of day ids
        user_res = requests.get(get_user_id_url + u_id,
            params = {'code': host_key})      

        planner_id = json.loads(user_res.text)["planner_id"]

        user_planner_res = requests.get(get_planner_url + str(planner_id), params = {'code': host_key})

        day_id_list = eval(user_planner_res.text.replace("'", '"'))['day_id_list']
            
        # need to turn list of day ids to list of days, then assign to day_list below
        day_list =[]
        sunday_event_list = events_from_day_id(day_id_list[0])
        monday_event_list = events_from_day_id(day_id_list[1])
        tuesday_event_list = events_from_day_id(day_id_list[2])
        wednesday_event_list = events_from_day_id(day_id_list[3])
        thursday_event_list = events_from_day_id(day_id_list[4])
        friday_event_list = events_from_day_id(day_id_list[5])
        saturday_event_list = events_from_day_id(day_id_list[6])

        return fl.render_template('main.html', day_list_url=fl.url_for('day_routes.day_list'),
            create_day_url=fl.url_for('day_routes.create_day'), event_list_url=fl.url_for('event_routes.event_list'),
            create_event_url=fl.url_for('event_routes.create_event'), planner_list_url=fl.url_for('planner_routes.planner'),
            create_planner_url=fl.url_for('planner_routes.create_planner'), share_planner_url=fl.url_for('user_routes.share_planner', id=u_id),
            current_user = current_user, sunday_event_list=sunday_event_list, monday_event_list=monday_event_list, 
            tuesday_event_list=tuesday_event_list, wednesday_event_list=wednesday_event_list, thursday_event_list=thursday_event_list, 
            friday_event_list=friday_event_list, saturday_event_list=saturday_event_list, friends_planner_url=fl.url_for('user_routes.friends_planner'))


def append_event_list(event_list, day_id, username):
    day_id_list_event_list = events_from_day_id(day_id)
    for event in day_id_list_event_list:
        event['title'] = username + ": " + event['title']
        event_list.append(event)


@user_routes.route('/friends_planner')
@login_required
def friends_planner():
    u_id = current_user.id
    
    user_dict = json.loads(requests.get(get_user_id_url + u_id, params={
        'code':host_key}).text)

    friends_list = user_dict['friends']

    get_planners_res = requests.get(get_planners_url,
        params = {'code': host_key})
    matched = ""

    sunday_event_list = []
    monday_event_list = []
    tuesday_event_list = []
    wednesday_event_list = []
    thursday_event_list = []
    friday_event_list = []
    saturday_event_list = []

    for friend_id in friends_list:
        for planner in eval(get_planners_res.text.replace("'", '"')):
            if friend_id == planner["user_id"]:
                matched = planner["_id"]
        get_single_planner_res = requests.get(get_planner_url + str(matched), 
            params = {'code': host_key})                        
        single_planner = eval(get_single_planner_res.text)
        day_id_list = single_planner['day_id_list']        

        friend_dict = json.loads(requests.get(get_user_id_url + friend_id, 
            params = {'code': host_key}).text)

        friend_username = friend_dict['username']

        append_event_list(sunday_event_list, day_id_list[0], friend_username)
        append_event_list(monday_event_list, day_id_list[1], friend_username)
        append_event_list(tuesday_event_list, day_id_list[2], friend_username)
        append_event_list(wednesday_event_list, day_id_list[3], friend_username)
        append_event_list(thursday_event_list, day_id_list[4], friend_username)
        append_event_list(friday_event_list, day_id_list[5], friend_username)
        append_event_list(saturday_event_list, day_id_list[6], friend_username)
    
    return fl.render_template('friends_planner.html', day_list_url=fl.url_for('day_routes.day_list'),
        create_day_url=fl.url_for('day_routes.create_day'), event_list_url=fl.url_for('event_routes.event_list'),
        create_event_url=fl.url_for('event_routes.create_event'), planner_list_url=fl.url_for('planner_routes.planner'),
        create_planner_url=fl.url_for('planner_routes.create_planner'), share_planner_url=fl.url_for('user_routes.share_planner', id=u_id),
        current_user = current_user, sunday_event_list=sunday_event_list, monday_event_list=monday_event_list, 
        tuesday_event_list=tuesday_event_list, wednesday_event_list=wednesday_event_list, thursday_event_list=thursday_event_list, 
        friday_event_list=friday_event_list, saturday_event_list=saturday_event_list)


def events_from_day_id(day_id):
    get_day_res = requests.get(get_day_url + day_id, params={
        'code':host_key})
    day_dict = json.loads(get_day_res.text)
    event_id_list = day_dict.get('event_id_list')
    event_dict_list = []
    for event in range(len(event_id_list)):
        get_event_res = requests.get(get_event_url + event_id_list[event], 
            params = {'code' : host_key})
        event_dict = json.loads(get_event_res.text)
        event_dict_list.append(event_dict)
    return event_dict_list

def day_id_to_day(day_id):
        get_day_res = requests.get(get_day_url + day_id, 
            params = {'code':host_key})
        day_dict = json.loads(get_day_res.text)
        return day_dict.get('day_name')

@user_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return fl.redirect(url_for('index'))

@user_routes.route('/user/')
@login_required
def user_list():
    
    res = requests.get(get_users_url, 
        params = {'code': host_key})

    return fl.render_template('user_list.html',userlist=json.loads(res.text))


@user_routes.route('/user/<username>', methods=["GET"])
@login_required
def user(username):
    u_id = current_user.id
    res = requests.get(get_user_id_url + username, 
        params = {'code': host_key})
    if 'admin' in current_user.roles:
        return fl.render_template('admin_user_data.html',user=json.loads(res.text))
    else:
        return fl.render_template('user_data.html', share_planner_url=fl.url_for('user_routes.share_planner', id=u_id), 
                friends_planner_url=fl.url_for('user_routes.friends_planner'), create_event_url=fl.url_for('event_routes.create_event'),
                user=json.loads(res.text))


@user_routes.route('/signup/', methods=["POST", "GET"])
def signup():
    
    if request.method == "GET":
        if current_user.is_anonymous:
            return fl.render_template('signup.html')
        elif 'admin' in current_user.roles:
            return fl.render_template('admin_create_user.html')
        else:
            return fl.render_template('signup.html')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Username and Password Are Required.')
            if current_user.is_anonymous:
                return fl.render_template('signup.html')
            elif 'admin' in current_user.roles:
                return fl.render_template('admin_create_user.html')
            else:
                return fl.render_template('signup.html')
        
        # Check if the username is already taken
        res = requests.post(add_user_url, json = {
            "username":username,
            "password":password,
            "friends":[]},
            params = {'code': host_key})

        if res.status_code == 201 and res.text == str(-1):
            flash('Username Already Taken')
            return fl.render_template('signup.html')
        
        
        else:
            u = user_model.authenticate(username, password)
            user = user_model.User(u.get('username'),u.get('_id'))
            login_user(user)

            planner = requests.post(add_planner_url, json = {
			    'day_id_list' : [],
			    'user_id' : res.text},
                params = {'code': host_key})
            day_ids = []
            for i in range(0, 7):
                day_name = ""
                if i == 0:
                    day_name = "Sunday"
                elif i == 1:
                    day_name = "Monday"
                elif i == 2:
                    day_name = "Tuesday"
                elif i == 3:
                    day_name = "Wednesday"
                elif i == 4:
                    day_name = "Thursday"
                elif i == 5:
                    day_name = "Friday"
                elif i == 6:
                    day_name = "Saturday"
                day_res = requests.post(add_day_url, json= {
                    'day_name': day_name,
                    'event_id_list': [],
                    'planner_id': planner.text
                }, params={'code': host_key})
                day_ids.append(day_res.text)

            requests.put(update_planner_url + planner.text, json = {
			    'attr' : "day_id_list",
			    'value' : day_ids},
                params = {'code': host_key})

            funni = requests.put(update_user_url + res.text, json = {
                'attr': 'planner_id',
                'val': planner.text}, 
                params = {'code': host_key})

            return fl.redirect(url_for('user_routes.home'))


@user_routes.route('/delete_user/<id>', methods=["POST"])
@login_required
def delete_user(id):
    
    text = request.form.get('delete')
    
    if text == 'delete':
        user_res = requests.get(get_user_id_url+id, params={
        'code':host_key})
        user_dict = json.loads(user_res.text)
        planner_id = user_dict.get('planner_id')
        planner_res = requests.get(get_planner_url + str(planner_id), 
            params = {'code': host_key})
    

        print("planner dictionary?", planner_res.text)
        planner_dict = eval(planner_res.text.replace("'", '"'))

        
        day_id_list = planner_dict['day_id_list']
        day_list = [] #this is a list of day dictionaries
        for day in range(0,7):
            get_day_res = requests.get(get_day_url + day_id_list[day], 
                params = {'code': host_key})
            day_dict = json.loads(get_day_res.text)
            day_list.append(day_dict)
        
        event_id_list = [] #this is a list of event_id_list from each day- all the user's events
        for day in day_list:
            event_list = (day.get('event_id_list'))
            for event_id in event_list:
                event_id_list.append(event_id)
        
        success = True
        
        #delete all user's events
        for event_id in event_id_list:
            response = requests.delete(delete_event_url + event_id, 
                params = {'code': host_key})
            if response.status_code != 200:
                success = False
                
        #delete all user's days
        for day_id in day_id_list:
            response = requests.delete(delete_day_url + day_id, 
                params= {'code': host_key})
            if response.status_code != 200:
                success = False
        
        #delete user's planner
        p_response = requests.delete(delete_planner_url + str(planner_id), 
            params = {'code': host_key})
        print("planner code", p_response.status_code)
        if p_response.status_code != 200:
            success = False
            
        #delete user
        u_response = requests.delete(delete_user_url+id, params={'code':host_key})
        if u_response.status_code != 200:
            success = False
        
        #something didn't delete properly
        if success == False:
            flash("Failed to Delete User")
            
        #all deletes succeeded
        else:
            flash('User Deleted Successfully!')
            
        return fl.redirect(url_for('user_routes.login'))
    
    else:
        flash('Delete Failed, Incorrect Input')
        return fl.redirect(fl.url_for('user_routes.user', username=id))


@user_routes.route('/update_user/<id>', methods=["GET", "POST"])
@login_required
def update_user(id):
    u_id = current_user.id
    if request.method == "GET":
        res = requests.get(get_user_id_url + id, 
            params = {'code': host_key})
        if 'admin' in current_user.roles:
            return fl.render_template('admin_update_user.html',user=json.loads(res.text))
        else:
            return fl.render_template('update_user.html', share_planner_url=fl.url_for('user_routes.share_planner', id=u_id), 
                friends_planner_url=fl.url_for('user_routes.friends_planner'), create_event_url=fl.url_for('event_routes.create_event'),
                user=json.loads(res.text))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    
        if username != '':
            response = requests.put(update_user_url + id, json = {
                'attr': 'username',
                'val': username}, 
                params = {'code': host_key})

        if password != '':
            response = requests.put(update_user_url + id, json = {
                'attr': 'password',
                'val': password}, 
                params = {'code': host_key})       

        if response.status_code == 200:
            flash('User Updated Successfully!', 'success')
        else:
            flash('Failed to Update Uer', 'error')
        
    return fl.redirect(url_for('user_routes.home'))


@user_routes.route('/share_planner/<id>', methods=["GET", "POST"])
@login_required
def share_planner(id):
    if request.method == "GET":
        res = requests.get(get_user_id_url + id, 
            params = {'code': host_key})

        return fl.render_template('share_planner.html', user=json.loads(res.text), friends_planner_url=fl.url_for('user_routes.friends_planner'), create_event_url=fl.url_for('event_routes.create_event'))
    
    if request.method == 'POST':
        username = request.form['username']
    
        if username != '':
            friend_dict = json.loads(requests.get(get_user_username_url + username, 
                params = {'code': host_key}).text)

            if friend_dict == None:
                flash('Failed to Share Planner', 'error')  
            else:

                friend_dict['friends'].append(id)
                
                friend_friends = friend_dict['friends']

                response = requests.put(update_user_url + friend_dict['_id'], json = {
                    'attr': 'friends',
                    'val': friend_friends}, 
                    params = {'code': host_key})   

                if response.status_code == 200:
                    flash('Planner Shared Successfully', 'success')
                else:
                    flash('Failed to Share Planner', 'error')
        
    return fl.redirect(url_for('user_routes.home'))
