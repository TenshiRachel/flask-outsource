import config.constants
from flask import Blueprint, render_template, request, url_for, redirect, flash, session
from models.service import Service


service_bp = Blueprint('service', __name__, template_folder=config.constants.template_dir,
                       static_folder=config.constants.static_dir, static_url_path='public', url_prefix='/service')


@service_bp.route('/list')
def list_service():
    services = Service.select()
    return render_template('service/list.html', services=services)
