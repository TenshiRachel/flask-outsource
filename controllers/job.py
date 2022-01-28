import config.constants
from flask import Blueprint, render_template, request, url_for, redirect, flash, session
from datetime import date
from middlewares.auth import is_auth
from models.service import Service
from models.user import User
from models.job import Job
from models.notifications import Notification


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

        if job is not None:
            flash('Please wait for your previous request to be completed before requesting again', 'error')
            return redirect(url_for('service.list_service'))

        Job.create(sid=sid, name=service.name, uid=service_provider.id, uname=service_provider.username,
                   cid=user_id, cname=client.username, date=date.today().strftime('%d/%m/%Y'),
                   salary=service.price, remarks=remarks)

        Notification.create(uid=int(user_id), username=client.username, pid=service.id, title=service.name,
                            category='job', user=service_provider.id)

        flash('Request sent successfully, please wait for ' + service_provider.username + '\'s response', 'success')
        return redirect(url_for('service.list_service'))


@job_bp.route('/delete/<id>')
@is_auth
def cancel_or_reject(id):
    user_id = session['user_id']
    user = User.get_by_id(user_id)
    job = Job.get_by_id(id)
    service = Service.get_by_id(job.sid)

    query = Job.delete().where(Job.id == id)
    query.execute()
    flash('Request cancelled/rejected successfully', 'success')
    if user.acc_type == 'client':
        Notification.create(uid=user.id, username=user.username, pid=service.id, title=service.name,
                            category='request_cancel', user=service.uid)

        return redirect(url_for('service.req'))

    else:
        Notification.create(uid=user_id, username=user.username, pid=service.id, title=service.name,
                            category='job_reject', user=job.cid)

        return redirect(url_for('job.index'))


@job_bp.route('/accept/<id>')
@is_auth
def accept(id):
    user_id = session['user_id']
    user = User.get_by_id(user_id)
    if user.acc_type == 'client':
        flash('Unauthorized action', 'error')

    job = Job.get_by_id(id)
    service = Service.get_by_id(job.sid)
    query = Job.update(status='accepted').where(Job.id == id)
    query.execute()

    Notification.create(uid=user.id, username=user.username, pid=service.id, title=service.name, category='request',
                        user=job.cid)

    flash('Job accepted', 'success')
    return redirect(url_for('job.index'))


@job_bp.route('/submit/<id>')
@is_auth
def submit(id):
    user_id = session['user_id']
    user = User.get_by_id(user_id)
    if user.acc_type == 'client':
        flash('Unauthorized action', 'error')

    job = Job.get_by_id(id)
    service = Service.get_by_id(job.sid)
    query = Job.update(status='done').where(Job.id == id)
    query.execute()

    Notification.create(uid=user.id, username=user.username, pid=service.id, title=service.name,
                        category='request_complete', user=job.cid)

    flash('Job completed', 'success')
    return redirect(url_for('job.index'))

