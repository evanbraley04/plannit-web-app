import flask as fl
import user_model
from flask_login import LoginManager, current_user
from user_routes import user_routes
from day_routes import day_routes
from event_routes import event_routes
from planner_routes import planner_routes
from dotenv import load_dotenv
load_dotenv()
import os

app = fl.Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint(event_routes)
app.register_blueprint(day_routes)
app.register_blueprint(user_routes)
app.register_blueprint(planner_routes)
app.secret_key = os.getenv("FLASK_SECRET_KEY")


@login_manager.user_loader
def load_user(user_id):
    return user_model.User.get(user_id)


@app.route("/")
def index():
    
    if current_user and hasattr(current_user, 'username'):
        return fl.redirect(fl.url_for('user_routes.home'))
    else:
        return fl.redirect(fl.url_for("user_routes.login"))
