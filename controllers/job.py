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

    return render_template('job/index.html', jobs=jobs, user=user)


@job_bp.route('/add/<sid>', methods=['POST'])
@is_auth
def add(sid):
    user_id = session['user_id']
    if request.method == 'POST':
        service = Service.get_by_id(sid)
        service_provider = User.get_by_id(service.uid)
        client = User.get_by_id(user_id)
        remarks = request.form.get('remarks')
        job = Job.get_or_none(Job.cid == user_id, Job.sid == sid)

        if job:
            flash('Please wait for your previous request to be completed before requesting again', 'error')
            return redirect(url_for('service.list'))

        Job.create(sid=sid, name=service.name, uid=service_provider.id, uname=service_provider.username,
                   cid=user_id, cname=client.username, date=date.today().strftime('%d/%m/%Y'),
                   salary=service.price, remarks=remarks)

        flash('Request sent successfully, please wait for ' + service_provider.username + '\'s response', 'success')
        return redirect(url_for('service.list'))


@job_bp.route('delete/<id>', methods=['POST'])
@is_auth
def cancel_or_reject(id):
    user_id = session['user_id']
    user = User.get_by_id(user_id)
    if request.method == 'POST':
        query = Job.delete().where(Job.id == id)
        query.execute()
        flash('Request cancelled/rejected successfully', 'success')
        if user.acc_type == 'client':
            return redirect(url_for('service.request'))
        else:
            return redirect(url_for('job.index'))


@job_bp.route('accept/<id>', methods=['POST'])
@is_auth
def accept(id):
    if request.method == 'POST':
        user_id = session['user_id']
        user = User.get_by_id(user_id)
        if user.acc_type == 'client':
            flash('Unauthorized action', 'error')
        query = Job.update(status='accepted').where(Job.id == id)
        query.execute()
        flash('Job accepted', 'success')
        return redirect(url_for('job.index'))


@job_bp.route('submit/<id>', methods=['POST'])
@is_auth
def submit(id):
    if request.method == 'POST':
        user_id = session['user_id']
        user = User.get_by_id(user_id)
        if user.acc_type == 'client':
            flash('Unauthorized action', 'error')
        query = Job.update(status='done').where(Job.id == id)
        query.execute()
        flash('Job completed', 'success')
        return redirect(url_for('job.index'))

