import flask as fl
from dotenv import load_dotenv
load_dotenv()
import os

app = fl.Flask(__name__)

from planner_routes import planner_routes
app.register_blueprint(planner_routes)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

@app.route("/")
def index():
	return fl.render_template('planner_index.html')