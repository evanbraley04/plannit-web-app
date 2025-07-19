import flask as fl
import requests, json
from flask_login import login_user, logout_user, login_required, current_user
from flask import Flask, flash, redirect, render_template, request, url_for
from dotenv import load_dotenv
load_dotenv()
import os

add_day_url = os.getenv("ADD_DAY_AZURE_URL")
get_day_url = os.getenv("GET_DAY_AZURE_URL")
get_days_url = os.getenv("GET_DAYS_AZURE_URL")
update_day_url = os.getenv("UPDATE_DAY_AZURE_URL")
delete_day_url = os.getenv("DELETE_DAY_AZURE_URL")
host_key = os.getenv("AZURE_FUNCTION_HOST_KEY")

day_routes = fl.Blueprint('day_routes', __name__, template_folder='templates')

@day_routes.route('/day/')
def day_list():

    res = requests.get(get_days_url, 
        params = {'code': host_key})
    return fl.render_template('day_list.html', daylist = json.loads(res.text))


@day_routes.route("/day/<_id>", methods=["GET"])
@login_required
def day(_id):
    res = requests.get(get_day_url+_id, 
        params = {'code': host_key})
    return fl.render_template('day_data.html', day = json.loads(res.text))

@day_routes.route('/create_day/', methods=['POST', 'GET'])
@login_required
def create_day():
    if request.method == "GET":
        return fl.render_template('create_day.html')

    if (request.method == 'POST'):
        day_name = request.form['day_name']
        s = request.form['event_id_list'] 
        event_id_list = []
        length = len(s)
        count = 0
        comma = 0
        word=""
        for char in request.form['event_id_list']:
            count+=1
            if char == ' ': #if its a space, make sure new word can be started
                if comma == 1:
                    word=""
                    comma = 0
                else:
                    word+=char
            elif char == ',': #if its a comma, this is end of word, add to list
                comma = 1
                event_id_list+= [word]
            else: #if its a letter, its part of word, add to word
                word+= char
                if count == length:
                    event_id_list+=[word]
        planner_id = request.form['planner_id']
        if day_name == '' or event_id_list == '' or planner_id == '':
            flash('Day Information Needed')
        else:
            res = requests.post(add_day_url, json = {
                'day_name': day_name, 
                'event_id_list': event_id_list,
                'planner_id': planner_id}, 
                params = {'code': host_key})
            flash('Added day')
            if (res.status_code != 201):
                flash('Day Creation Failed')
    
    _id = res.text
    return fl.redirect(fl.url_for('day_routes.day', _id=_id))

@day_routes.route('/delete_day/<_id>', methods=['POST'])
@login_required
def delete_day(_id):
    delete = request.form.get('delete')
    if delete == 'delete':
        res = requests.delete(delete_day_url+_id, 
            params = {'code': host_key})
        if res.status_code == 200:
            flash("Successfully Deleted Day")
        else:
            flash("Failed to Delete Day")
        return fl.redirect(fl.url_for('day_routes.day_list'))
    else:
        flash("Failed, Incorrect Input Received")
        return fl.redirect(fl.url_for('day_routes.day', _id=_id))
    

@day_routes.route('/update_day/<_id>', methods=['GET', 'POST'])
@login_required
def update_day(_id):
    if request.method == "GET":
        res = requests.get(get_day_url+_id, 
            params = {'code': host_key})
        return fl.render_template('update_day.html', day=json.loads(res.text))
    elif request.method == "POST":
        day_name = request.form['day_name']
        if day_name != '': #if it is unempty
            response = requests.put(update_day_url+_id, json = {
                'attribute': 'day_name',
                'value': day_name}, 
                params = {'code': host_key})
        if response.status_code == 200:
            flash("Day Updated Successfully")
        else:
            flash("Failed to Update Day")

    return fl.redirect(url_for('day_routes.day_list', _id=response.text))