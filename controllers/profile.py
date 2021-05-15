import config.constants
from flask import Blueprint, render_template, request, url_for, redirect, flash, session
from middlewares.auth import is_auth
from models.service import Service
from models.user import User

profile_bp = Blueprint('profile', __name__, template_folder=config.constants.template_dir,
                       static_folder=config.constants.static_dir, static_url_path='public', url_prefix='/user')


@profile_bp.route('/profile')
@is_auth
def profile():
    user_id = session['user_id']
    user = User.get_by_id(user_id)
    return render_template('profile/index.html', user=user)
