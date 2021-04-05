import config.constants
from flask import Blueprint, render_template, request, url_for, redirect, flash, session
from datetime import date
from middlewares.auth import is_auth
from models.service import Service
from models.user import User


service_bp = Blueprint('service', __name__, template_folder=config.constants.template_dir,
                       static_folder=config.constants.static_dir, static_url_path='public', url_prefix='/service')


@service_bp.route('/list')
def list_service():
    services = Service.select()
    return render_template('service/list.html', services=services)


@service_bp.route('/manage')
@is_auth
def manage():
    user_id = session['user_id']

    if User.get(User.id == user_id).acc_type == 'client':
        flash('You need a service provider account to manage services', 'error')
        redirect(url_for('index.index'))

    services = Service.select().where(Service.uid == user_id)
    return render_template('service/manage.html', services=services)


@service_bp.route('/add', methods=['GET', 'POST'])
@is_auth
def add():
    user_id = session['user_id']

    if User.get(User.id == user_id).acc_type == 'client':
        flash('You need a service provider account to add service', 'error')
        redirect(url_for('index.index'))

    if request.method == 'POST':
        req = request.form

        name = req.get('name')
        desc = req.get('desc')
        price = req.get('price')
        categories = req.getlist('categories')

        Service.create(name=name, desc=desc, price=price, categories=categories,
                       date_created=date.today().strftime('%d/%m/%Y'),
                       views=0, favs=0, uid=user_id)

        flash('Service created successfully', 'success')
        redirect(url_for('service.manage'))

    return render_template('service/add.html')
