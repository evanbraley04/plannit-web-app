import flask as fl
import requests, json
from flask_login import login_user, logout_user, login_required, current_user
from bson import ObjectId
from dotenv import load_dotenv
load_dotenv()
import os

add_planner_url = os.getenv('ADD_PLANNER_AZURE_URL')
get_planner_url = os.getenv("GET_PLANNER_AZURE_URL") 
get_planners_url = os.getenv("GET_PLANNERS_AZURE_URL")
update_planner_url = os.getenv("UPDATE_PLANNER_AZURE_URL")
delete_planner_url = os.getenv("DELETE_PLANNER_AZURE_URL")

host_key = os.getenv("AZURE_FUNCTION_HOST_KEY")

planner_routes = fl.Blueprint('planner_routes', __name__, template_folder='templates')

@planner_routes.route('/planner/', defaults={'planner_id': None})
@login_required
def planner(planner_id=None):
	
	def chew(raw_planner):
		#use to convert raw list of planners to be more digestable for Jinja
		return {"id" : str(raw_planner['_id'])}
	
	get_res = requests.get(get_planners_url,
		params = {'code': host_key})
	
	text = get_res.text
	list = eval(text)
	
	return fl.render_template("planner.html", list_of_planners=map(chew, list))


@planner_routes.route("/planner/<planner_id>", methods=["GET"])
@login_required
def planner_days(planner_id):
	
	get_res = requests.get(get_planner_url + planner_id,
		params = {'code': host_key})
	text = get_res.text
	dict = eval(text)
	return fl.render_template("planner_days.html", planner_id=planner_id, user_id=dict['user_id'], list_of_days=dict['day_id_list'])

@planner_routes.route("/planner_create/", methods=["GET", "POST"])
@login_required
def create_planner():
	msg = ""
	
	if fl.request.method == "POST":
		# here, need to get the values submitted by the user and validate them
		# Then, return page with error message if wrong
		# Otherwise, send the user to the page with the list of users
		requests.post(add_planner_url, json={
			'day_id_list' : eval("[" + fl.request.form["lodays"] + "]"),
			'user_id' : fl.request.form["uid"]},
			params = {'code': host_key})
		msg = "it worked"
	return fl.render_template("planner_create.html", message=msg)

@planner_routes.route("/planner_delete/<planner_id>", methods=["GET", "POST"])
@login_required
def delete_planner(planner_id):
	msg = ""
	# (should verify user intention before simply deleting)
	if fl.request.method == "POST":
		requests.delete(delete_planner_url + planner_id,
			params = {'code': host_key})
		msg = "target eliminated (planner deleted)"
		planner_id = ""
	return fl.render_template("planner_delete.html", to_delete=planner_id, message=msg)

@planner_routes.route("/planner_update/<planner_id>", methods=["GET", "POST"])
@login_required
def update_planner(planner_id):
	msg = ""
	user = ""
	days = ""
	# use "POST" method call like used to create a planner above
	if fl.request.method == "POST":
		requests.put(update_planner_url + planner_id, json = {
			'attr' : "day_id_list",
			'value' : eval(fl.request.form["daylist"])},
			params = {'code': host_key})
		requests.put(update_planner_url + planner_id, json = {
			'attr' : "user_id",
			'value' : fl.request.form["userid"]},
			params = {'code': host_key})
		msg = "values have been updated"
	else:
		get_res = requests.get(get_planner_url + planner_id,
			params = {'code': host_key})
		text = get_res.text
		dict = eval(text)
		user = dict['user_id']
		days = str(dict['day_id_list'])
	return fl.render_template("planner_update.html", message=msg, to_modify=planner_id, days_in=days, user_id_in=user)