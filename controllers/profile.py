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
    user_id = session['user_id']
    if request.method == 'POST':
        req = request.form
        bio = req.get('bio')
        website = req.get('website')
        dob = req.get('dob')
        location = req.get('location')
        gender = req.get('gender')
        occupation = req.get('occupation')

        query = User.update(bio=bio, website=website, dob=dob, location=location, gender=gender, occupation=occupation)\
            .where(User.id == user_id)
        query.execute()
        flash('Changes saved successfully', 'success')
        return redirect(url_for('user.profile'))

    user = User.get_by_id(user_id)
    social_medias = user.social_medias.split(',')
    skills = user.skills.split(',')
    return render_template('profile/edit.html', user=user, social_medias=social_medias, skills=skills)


@profile_bp.route('/profile/delete/<id>')
@is_auth
def delete(id):
    user_id = session['user_id']
    if user_id != id:
        flash('You are not authorized to perform this action', 'error')
        return redirect(url_for('user.profile'))

    query = User.delete().where(User.id == user_id)
    query.execute()

    flash('Account deleted successfully', 'success')
    return redirect(url_for('index.index'))
