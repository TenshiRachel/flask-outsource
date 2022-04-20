import config.constants
from flask import Blueprint, render_template, request, url_for, redirect, flash, session
from middlewares.auth import is_auth
from models.service import Service
from models.portfolio import Portfolio
from models.user import User

profile_bp = Blueprint('profile', __name__, template_folder=config.constants.template_dir,
                       static_folder=config.constants.static_dir, static_url_path='public', url_prefix='/user')


@profile_bp.route('/view/<id>')
def view(id):
    user_id = session.get('user_id')
    user = User.get_or_none(User.id == user_id)

    viewuser = User.get_by_id(id)
    social_medias = viewuser.social_medias.split(',')
    follower_ids = viewuser.followers.split(',')
    following_ids = viewuser.following.split(',')
    followers = []
    if follower_ids[0] != '':
        for id in follower_ids:
            followers.append(User.get_by_id(id))
    following = []
    if following_ids[0] != '':
        for id in following_ids:
            following.append(User.get_by_id(id))
    skills = viewuser.skills.split(',')

    return render_template('profile/view.html', user=user, viewuser=viewuser, social_medias=social_medias,
                           followers=followers, following=following, skills=skills)


@profile_bp.route('/follow/<uid>')
@is_auth
def follow(uid):
    if uid is None:
        flash('User not found', 'error')
        return redirect(url_for('profile.view'))

    user_id = session['user_id']
    user = User.get_by_id(user_id)

    if uid == user_id:
        flash('You cannot follow yourself', 'error')
        return redirect(url_for('profile.view'))

    viewed_user = User.get_by_id(uid)

    user_follow_list = user.following.split(',')

    if uid in user_follow_list:
        flash('You are already following this user', 'error')
        return redirect(url_for('profile.view'))

    user_follow_list.append(uid)

    viewed_user_list = viewed_user.followers.split(',')
    viewed_user_list.append(user_id)

    query = User.update(following=','.join(user_follow_list)).where(User.id == user_id)
    query.execute()

    query = User.update(followers=','.join(viewed_user_list)).where(User.id == uid)
    query.execute()

    flash('User followed successfully', 'success')
    return redirect(url_for('profile.view'))


@profile_bp.route('/unfollow/<uid>')
@is_auth
def unfollow(uid):
    if uid is None:
        flash('User not found', 'error')
        return redirect(url_for('profile.view'))

    user_id = session['user_id']
    user = User.get_by_id(user_id)

    viewed_user = User.get_by_id(uid)

    user_follow_list = user.following.split(',')

    if uid not in user_follow_list:
        flash('You are not following this user', 'error')
        return redirect(url_for('profile.view'))

    user_follow_list.remove(uid)

    viewed_user_list = viewed_user.followers.split(',')
    viewed_user_list.remove(user_id)

    query = User.update(following=','.join(user_follow_list)).where(User.id == user_id)
    query.execute()

    query = User.update(followers=','.join(viewed_user_list)).where(User.id == uid)
    query.execute()

    flash('User unfollowed successfully', 'success')
    return redirect(url_for('profile.view'))


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

        banner = request.files['upload_banner']
        pic = request.files['upload_image']

        query = User.update(bio=bio, website=website, dob=dob, location=location, gender=gender, occupation=occupation)\
            .where(User.id == user_id)
        query.execute()

        banner.save(config.constants.uploads_dir + '/' + str(user_id) + '/profile/banner.png')
        pic.save(config.constants.uploads_dir + '/' + str(user_id) + '/profile/profilePic.png')

        flash('Changes saved successfully', 'success')
        return redirect(url_for('profile.view'))

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
        return redirect(url_for('profile.view'))

    query = User.delete().where(User.id == user_id)
    query.execute()

    flash('Account deleted successfully', 'success')
    return redirect(url_for('index.index'))

# TODO: Portfolios
