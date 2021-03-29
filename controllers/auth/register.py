import config.constants
from flask import Blueprint, render_template, request, url_for, redirect, flash
from wtforms import Form, StringField, PasswordField, validators
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
    errors = {}

    if request.method == 'POST':
        username = form.username.data
        email = form.email.data
        password = form.password.data
        cfm_pass = form.confirm.data

        if username == '':
            errors['username'] = 'Username is required'

        if email == '':
            errors['email'] = 'Email is required'

        if password == '':
            errors['password'] = 'Password is required'

        elif len(password) < 8:
            errors['password'] = 'Password must be at least 8 characters'

        if password != cfm_pass:
            errors['cfmPassword'] = 'Passwords do not match'

        if User.get_or_none(User.email == email) is not None:
            errors['account'] = 'An account with this email already exists'

        if len(errors) > 0:
            flash(', '.join(errors.values()), 'error')
            return redirect(url_for('auth.register'))

        user = User.create(username=username, email=email, password=password, acc_type='client')

        flash('You have registered successfully and can now log in', 'success')
        return redirect(url_for('index.index', user=user))

    return render_template('auth/register.html')
