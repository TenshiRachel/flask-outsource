from functools import wraps
from flask import session, flash, redirect, url_for


def is_auth(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'authenticated' in session:
            return f(*args, **kwargs)

        else:
            flash('Please sign in to view the page')
            return redirect(url_for('auth.login'))
