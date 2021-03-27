import config.constants
from flask import Blueprint, render_template
from models.user import User


auth_bp = Blueprint('auth', __name__, template_folder=config.constants.template_dir,
                    static_folder=config.constants.static_dir, static_url_path='public', url_prefix='/auth')


@auth_bp.route('/register')
def register():
    return render_template('auth/register.html')
