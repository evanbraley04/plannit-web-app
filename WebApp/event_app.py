import flask as fl
from dotenv import load_dotenv
load_dotenv()
import os

app = fl.Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

from event_routes import event_routes
app.register_blueprint(event_routes)

@app.route("/")
def index():
    return fl.render_template('index.html', event_list_url=fl.url_for('event_routes.event_list'), create_event_url=fl.url_for('event_routes.create_event'))