import config.constants
from flask import Flask
from flask_toastr import Toastr
from datetime import timedelta
from config.dbConnect import setupdb
from config.constants import app_secret_key
from controllers.index import index_bp
from controllers.auth import auth_bp
from controllers.service import service_bp
from controllers.job import job_bp
from controllers.profile import profile_bp
from controllers.files import files_bp
from controllers.notifications import notifications_bp


setupdb()
app = Flask(__name__, template_folder=config.constants.template_dir,
            static_folder=config.constants.static_dir, static_url_path='/public')


toastr = Toastr(app)
app.register_blueprint(index_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(service_bp)
app.register_blueprint(job_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(files_bp)
app.register_blueprint(notifications_bp)


if __name__ == "__main__":
    app.debug = True
    app.permanent_session_lifetime = timedelta(hours=2)
    app.secret_key = app_secret_key
    app.run()
