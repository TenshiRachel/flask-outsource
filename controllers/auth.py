import config.constants
from flask import Blueprint, render_template, request, url_for, redirect, flash, session
from models.user import User


auth_bp = Blueprint('auth', __name__, template_folder=config.constants.template_dir,
                    static_folder=config.constants.static_dir, static_url_path='public', url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    req = request.form
    errors = {}

    if request.method == 'POST':
        username = req.get('username')
        email = req.get('email')
        password = req.get('password')
        cfm_pass = req.get('cfmPassword')

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

        User.create(username=username, email=email, password=password, acc_type='client')

        flash('You have registered successfully and can now log in', 'success')
        return redirect(url_for('index.index'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    req = request.form
    errors = 0

    if request.method == 'POST':
        username = req.get('username')
        email = req.get('email')
        password = req.get('password')

        user = User.get_or_none(User.email == email)

        if user is None:
            flash('Account does not exist, please register', 'error')
            return redirect(url_for('auth.register'))

        if username == '':
            errors += 1

        if email == '':
            errors += 1

        if password == '':
            errors += 1

        if password != user.password:
            errors += 1

        if errors > 0:
            flash('Invalid sign in credentials', 'error')
            return redirect(url_for('auth.login'))

        session.permanent = True
        session['authenticated'] = True
        session['user_id'] = user.id
        flash('You have logged in successfully', 'success')
        return redirect(url_for('index.index'))

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have signed out successfully', 'success')
    return redirect(url_for('index.index'))
