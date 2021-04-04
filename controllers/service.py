import config.constants
from flask import Blueprint, render_template, request, url_for, redirect, flash, session
from middlewares.auth import is_auth
from models.service import Service


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
    services = Service.select().where(Service.uid == user_id)
    return render_template('service/manage.html', services=services)


@service_bp.route('/add', methods=['GET', 'POST'])
@is_auth
def add():
    if request.method == 'POST':
        req = request.form

        name = req.get('name')
        desc = req.get('desc')
        price = req.get('price')
        categories = req.get('categories')

        pass

    return render_template('service/add.html')
