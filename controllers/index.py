import config.constants
from flask import Blueprint, render_template, session
from models.user import User
from models.notifications import Notification


index_bp = Blueprint('index', __name__, template_folder=config.constants.template_dir,
                     static_folder=config.constants.static_dir, static_url_path='public', url_prefix='/')


@index_bp.route('/')
def index():
    if session.get('user_id') is not None:
        user = User.get_or_none(session['user_id'])
        notifications = Notification.select().where(Notification.user == user.id) if user is not None else None

        return render_template('index.html', user=user,  notifications=notifications)

    return render_template("index.html")
