import config.constants
from flask import Blueprint, render_template, request, url_for, redirect
from wtforms import Form, StringField, RadioField, IntegerField, FloatField, TextAreaField, PasswordField, validators
from models.user import User


auth_bp = Blueprint('auth', __name__, template_folder=config.constants.template_dir,
                    static_folder=config.constants.static_dir, static_url_path='public', url_prefix='/auth')


class RegisterForm(Form):
    username = StringField('name')
    email = StringField('email')
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.Length(min=8)
    ])
    confirm = PasswordField('confirm')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        user = User.create(username=username, email=email, password=password, acc_type='client')

        return redirect(url_for('index.index', user=user))

    return render_template('auth/register.html')
