import config.constants
from flask import Blueprint, render_template, session
from models.user import User


index_bp = Blueprint('index', __name__, template_folder=config.constants.template_dir,
                     static_folder=config.constants.static_dir, static_url_path='public', url_prefix='/')


@index_bp.route('/')
def index():
    if session.get('user_id') is not None:
        user = User.get_by_id(session['user_id'])
        return render_template('index.html', user=user)

    return render_template("index.html")
