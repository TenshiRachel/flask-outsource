import config.constants
from flask import Blueprint, render_template, request, url_for, redirect, flash, session
from datetime import date
from middlewares.auth import is_auth
from models.service import Service
from models.user import User
from models.job import Job


service_bp = Blueprint('service', __name__, template_folder=config.constants.template_dir,
                       static_folder=config.constants.static_dir, static_url_path='public', url_prefix='/service')


@service_bp.route('/list')
def list_service():
    user_id = session.get('user_id')
    user = User.get_or_none(User.id == user_id)
    services = Service.select()
    return render_template('service/list.html', services=services, user=user)


@service_bp.route('/view/<uid>/<id>')
def view(uid, id):
    user_id = session.get('user_id')
    user = User.get_or_none(User.id == user_id)
    service = Service.get_or_none(Service.id == id)
    if not service:
        flash('Service not found', 'error')
        return redirect(url_for('service.list'))
    service_user = User.get_by_id(uid)
    job = Job.get_or_none(Job.sid == id, Job.cid == user_id)

    query = Service.update(views=service.views + 1).where(Service.id == id)
    query.execute()
    return render_template('service/index.html', services=service, service_user=service_user, user=user, job=job)


@service_bp.route('/fav/<id>', methods=['POST'])
@is_auth
def fav(id):
    if request.method == 'POST':
        service = Service.get_or_none(Service.id == id)

        if service is None:
            flash('Service not found', 'error')
            return redirect(url_for('service.list'))

        flash('Service favorited', 'success')
        return redirect(url_for('service.list'))


@service_bp.route('/manage')
@is_auth
def manage():
    user_id = session['user_id']
    user = User.get_by_id(user_id)

    if user.acc_type == 'client':
        flash('You need a service provider account to manage services', 'error')
        return redirect(url_for('index.index'))

    services = Service.select().where(Service.uid == user_id)
    return render_template('service/manage.html', services=services, user=user)


@service_bp.route('/request')
@is_auth
def req():
    user_id = session['user_id']
    user = User.get_by_id(user_id)
    jobs = Job.select().where(Job.cid == user_id)

    if user.acc_type != 'client':
        flash('You need a client account to request a service', 'error')
        redirect(url_for('service.list'))

    return render_template('service/request.html', jobs=jobs, user=user)


@service_bp.route('/add', methods=['GET', 'POST'])
@is_auth
def add():
    user_id = session['user_id']
    user = User.get_by_id(user_id)

    if user.acc_type == 'client':
        flash('You need a service provider account to add services', 'error')
        return redirect(url_for('index.index'))

    if request.method == 'POST':
        req = request.form

        name = req.get('name')
        desc = req.get('desc')
        price = req.get('price')
        categories = req.getlist('categories')
        categories = ' '.join(categories)
        poster = request.files('poster')

        Service.create(name=name, desc=desc, price=price, categories=categories,
                       date_created=date.today().strftime('%d/%m/%Y'),
                       views=0, favs=0, username=user.username, uid=user_id)
        poster.save(config.constants.uploads_dir + '/' + user.id + '/profilePic.png')

        flash('Service created successfully', 'success')
        return redirect(url_for('service.manage'))

    return render_template('service/add.html', user=user)


@service_bp.route('/edit/<id>', methods=['GET', 'POST'])
@is_auth
def edit(id):
    services = Service.get_or_none(Service.id == id)
    user_id = session['user_id']
    user = User.get_by_id(user_id)

    if user.acc_type == 'client':
        flash('You need a service provider account to edit services', 'error')
        return redirect(url_for('index.index'))

    if services is None:
        flash('Service not found', 'error')
        return redirect(url_for('service.manage'))

    if request.method == 'POST':
        req = request.form

        name = req.get('name')
        desc = req.get('desc')
        price = req.get('price')
        categories = req.getlist('categories')
        categories = ' '.join(categories)

        query = Service.update(name=name, desc=desc, price=price, categories=categories).where(Service.id == id)
        query.execute()
        flash('Changes saved successfully', 'success')
        return redirect(url_for('service.manage'))

    return render_template('service/edit.html', services=services, user=user)


@service_bp.route('/delete/<id>')
@is_auth
def delete(id):
    if Service.get_or_none(Service.id == id) is None:
        flash('Service not found', 'error')
        return redirect(url_for('service.manage'))

    query = Service.delete().where(Service.id == id)
    query.execute()
    flash('Service deleted successfully', 'success')
    return redirect(url_for('service.manage'))
