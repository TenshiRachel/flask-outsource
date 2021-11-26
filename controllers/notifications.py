import config.constants
from flask import Blueprint, render_template, request, url_for, redirect, flash, session
from middlewares.auth import is_auth
from models.user import User
from models.notifications import Notification

notifications_bp = Blueprint('notifications', __name__, template_folder=config.constants.template_dir,
                             static_folder=config.constants.static_dir, static_url_path='public',
                             url_prefix='/notifications')


@notifications_bp.route('/')
@is_auth
def index():
    user_id = session.get('user_id')
    user = User.get_by_id(user_id)

    like_notifications = Notification.select().where(Notification.user == user_id & Notification.category == 'likes')\
        .order_by(Notification.date.desc())

    return render_template('notifications/index.html', user=user, like_notifications=like_notifications)
