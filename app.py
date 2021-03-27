import config.constants
from flask import Flask, render_template
from config.dbConnect import setupdb
from controllers.auth.register import auth_bp


setupdb()
app = Flask(__name__, template_folder=config.constants.template_dir,
            static_folder=config.constants.static_dir, static_url_path='/public')


@app.route("/")
def index():
    return render_template("index.html")


app.register_blueprint(auth_bp)


if __name__ == "__main__":
    app.debug = True
    app.run()
