import config.constants
from flask import Blueprint, render_template, request, url_for, redirect, flash, session
from datetime import date
from middlewares.auth import is_auth
from models.service import Service
from models.user import User
from models.job import Job


job_bp = Blueprint('job', __name__, template_folder=config.constants.template_dir,
                    static_folder=config.constants.static_dir, static_url_path='public', url_prefix='/job')


@job_bp.route('/index', methods=['GET', 'POST'])
@is_auth
def index():
    user_id = session['user_id']
    user = User.get_by_id(user_id)
    jobs = Job.select().where(Job.uid == user_id)

    if request.method == 'POST':
        pass

    return render_template('job/index.html', jobs=jobs)

