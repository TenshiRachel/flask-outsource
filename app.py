import os
from flask import Flask, render_template
from config.dbConnect import setupdb
from controllers.auth.register import auth_bp


setupdb()
template_dir = os.path.abspath('views')
static_dir = os.path.abspath('public')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir, static_url_path='/public')


@app.route("/")
def index():
    return render_template("index.html")


app.register_blueprint(auth_bp)


if __name__ == "__main__":
    app.debug = True
    app.run()
