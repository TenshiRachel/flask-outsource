import config.constants
from flask import Blueprint, render_template


index_bp = Blueprint('index', __name__, template_folder=config.constants.template_dir,
                     static_folder=config.constants.static_dir, static_url_path='public', url_prefix='/')


@index_bp.route('/')
def index():
    return render_template("index.html")
