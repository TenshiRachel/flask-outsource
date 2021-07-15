import config.constants
from flask import Blueprint, render_template, request, url_for, redirect, flash, session
from middlewares.auth import is_auth
from models.user import User
from models.files import File


files_bp = Blueprint('files', __name__, template_folder=config.constants.template_dir,
                     static_folder=config.constants.static_dir, static_url_path='public', url_prefix='/files')


@files_bp.route('/manage')
@is_auth
def manage():
    user_id = session.get('user_id')
    user = User.get_by_id(user_id)
    files = File.select().where(File.uid == user_id)

    return render_template('files/index.html', user=user)
