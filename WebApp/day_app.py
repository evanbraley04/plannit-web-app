import flask as fl
from dotenv import load_dotenv
load_dotenv()
import os

app = fl.Flask(__name__)

from day_routes import day_routes
app.register_blueprint(day_routes)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

@app.route("/")
def index():
    return fl.render_template('index.html', day_url = fl.url_for('day_routes.day_list'))

