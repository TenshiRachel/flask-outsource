import config.constants
from flask import Flask
from config.dbConnect import setupdb
from controllers.index import index_bp
from controllers.auth.register import auth_bp


setupdb()
app = Flask(__name__, template_folder=config.constants.template_dir,
            static_folder=config.constants.static_dir, static_url_path='/public')


app.register_blueprint(index_bp)
app.register_blueprint(auth_bp)


if __name__ == "__main__":
    app.debug = True
    app.run()
