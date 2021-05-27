import config.constants
from flask import Blueprint, render_template, request, url_for, redirect, flash, session
from middlewares.auth import is_auth
from models.service import Service
from models.user import User

profile_bp = Blueprint('profile', __name__, template_folder=config.constants.template_dir,
                       static_folder=config.constants.static_dir, static_url_path='public', url_prefix='/user')


@profile_bp.route('/profile')
@is_auth
def profile():
    user_id = session['user_id']
    user = User.get_by_id(user_id)
    social_medias = user.social_medias.split(',')
    follower_ids = user.followers.split(',')
    following_ids = user.following.split(',')
    followers = []
    if follower_ids[0] != '':
        for id in follower_ids:
            followers.append(User.get_by_id(id))
    following = []
    if following_ids[0] != '':
        for id in following_ids:
            following.append(User.get_by_id(id))
    skills = user.skills.split(',')
    return render_template('profile/index.html', user=user, social_medias=social_medias,
                           followers=followers, following=following, skills=skills)


@profile_bp.route('/profile/edit', methods=['GET', 'POST'])
@is_auth
def edit():
    if request.method == 'POST':
        req = request.form
        pass

    user_id = session['user_id']
    user = User.get_by_id(user_id)
    social_medias = user.social_medias.split(',')
    skills = user.skills.split(',')
    return render_template('profile/edit.html', user=user, social_medias=social_medias, skills=skills)
