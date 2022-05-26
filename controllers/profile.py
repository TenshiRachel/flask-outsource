import config.constants
from flask import Blueprint, render_template, request, url_for, redirect, flash, session
from middlewares.auth import is_auth
from models.service import Service
from models.portfolio import Portfolio
from models.user import User
from models.notifications import Notification

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

    projects = Portfolio.select().where(Portfolio.uid == viewuser.id)
    services = Service.select().where(Service.uid == viewuser.id)

    return render_template('profile/view.html', user=user, viewuser=viewuser, social_medias=social_medias,
                           followers=followers, following=following, skills=skills, projects=projects,
                           services=services)


@profile_bp.route('/follow/<uid>')
@is_auth
def follow(uid):
    user_id = session['user_id']
    user = User.get_by_id(user_id)

    if uid is None:
        flash('User not found', 'error')
        return redirect(url_for('profile.view', id=user_id))

    if uid == user_id:
        flash('You cannot follow yourself', 'error')
        return redirect(url_for('profile.view', id=user_id))

    viewed_user = User.get_by_id(uid)

    user_follow_list = user.following.split(',')

    if uid in user_follow_list:
        flash('You are already following this user', 'error')
        return redirect(url_for('profile.view', id=user_id))

    user_follow_list.append(uid)

    viewed_user_list = viewed_user.followers.split(',')
    viewed_user_list.append(user_id)

    query = User.update(following=','.join(user_follow_list)).where(User.id == user_id)
    query.execute()

    query = User.update(followers=','.join(viewed_user_list)).where(User.id == uid)
    query.execute()

    Notification.create(uid=int(user_id), username=user.username, category='follow', user=viewed_user.id)

    flash('User followed successfully', 'success')
    return redirect(url_for('profile.view', id=user_id))


@profile_bp.route('/unfollow/<uid>')
@is_auth
def unfollow(uid):
    user_id = session['user_id']
    user = User.get_by_id(user_id)

    if uid is None:
        flash('User not found', 'error')
        return redirect(url_for('profile.view', id=user_id))

    viewed_user = User.get_by_id(uid)

    user_follow_list = user.following.split(',')

    if uid not in user_follow_list:
        flash('You are not following this user', 'error')
        return redirect(url_for('profile.view', id=user_id))

    user_follow_list.remove(uid)

    viewed_user_list = viewed_user.followers.split(',')
    viewed_user_list.remove(user_id)

    query = User.update(following=','.join(user_follow_list)).where(User.id == user_id)
    query.execute()

    query = User.update(followers=','.join(viewed_user_list)).where(User.id == uid)
    query.execute()

    flash('User unfollowed successfully', 'success')
    return redirect(url_for('profile.view', id=user_id))


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
        return redirect(url_for('profile.view', id=user_id))

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
        return redirect(url_for('profile.view', id=user_id))

    query = User.delete().where(User.id == user_id)
    query.execute()

    flash('Account deleted successfully', 'success')
    return redirect(url_for('index.index'))


@profile_bp.route('/project/add', methods=['GET', 'POST'])
@is_auth
def create_project():
    user_id = session['user_id']
    user = User.get_by_id(user_id)

    if request.method == 'POST':
        req = request.form
        title = req.get('title')
        content = req.get('content')
        category = req.getlist('projectCategory')
        category = ','.join(category)
        cover = request.files['coverPicture']

        project = Portfolio.create(title=title, content=content, category=category, uid=int(user_id))
        cover.save(config.constants.uploads_dir + '/' + str(user_id) + '/projects/' + str(project.id) + '.png')

        flash('Project added successfully', 'success')
        return redirect(url_for('profile.view', id=user_id))

    return render_template('profile/add_project.html', user=user)


@profile_bp.route('/project/edit/<id>', methods=['GET', 'POST'])
@is_auth
def edit_project(id):
    user_id = session['user_id']
    user = User.get_by_id(user_id)
    if id is None:
        flash('Project could not be found', 'error')
        return redirect(url_for('profile.view', id=user_id))

    project = Portfolio.get_by_id(id)

    if user.id != project.uid:
        flash('You are unauthorized to perform actions on this project', 'error')
        return redirect(url_for('profile.view', id=user_id))

    if request.method == 'POST':
        req = request.form
        title = req.get('title')
        content = req.get('content')
        category = req.getlist('projectCategory')
        category = ','.join(category)
        cover = request.files['coverPicture']

        query = Portfolio.update(title=title, content=content, category=category).where(Portfolio.id == id)
        query.execute()
        cover.save(config.constants.uploads_dir + '/' + str(user_id) + '/projects/' + str(project.id) + '.png')

        flash('Project updated successfully', 'success')
        return redirect(url_for('profile.view', id=user_id))

    return render_template('profile/edit_project.html', user=user, project=project)


@profile_bp.route('/project/delete/<id>')
@is_auth
def delete_project(id):
    user_id = session['user_id']

    if id is None:
        flash('Please select a project to delete', 'error')
        return redirect(url_for('profile.view', id=user_id))

    project = Portfolio.get_by_id(id)
    if user_id != project.uid:
        flash('You are unauthorized to perform actions on this project', 'error')
        return redirect(url_for('profile.view', id=user_id))

    query = Portfolio.delete().where(Portfolio.id == id)
    query.execute()

    flash('Project deleted successfully', 'success')
    return redirect(url_for('profile.view', id=user_id))
