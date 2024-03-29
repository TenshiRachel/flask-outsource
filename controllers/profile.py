import config.constants
from flask import Blueprint, render_template, request, url_for, redirect, flash, session
from middlewares.auth import is_auth
from models.service import Service
from models.portfolio import Portfolio
from models.comment import Comment
from models.user import User
from models.notifications import Notification
from models.followers import Follower

profile_bp = Blueprint('profile', __name__, template_folder=config.constants.template_dir,
                       static_folder=config.constants.static_dir, static_url_path='public', url_prefix='/user')


@profile_bp.route('/view/<id>')
def view(id):
    user_id = session.get('user_id')
    user = User.get_or_none(User.id == user_id)
    viewuser = User.get_by_id(id)
    social_medias = viewuser.social_medias.split(',')
    notifications = Notification.select().where(Notification.user == viewuser.id)

    # TODO: Function to optimize notifications, shorten skills

    followers = User.select().join(Follower, on=(User.id == Follower.follower_id))\
        .where(Follower.following_id == viewuser.id)

    following = User.select().join(Follower, on=(User.id == Follower.following_id))\
        .where(Follower.follower_id == viewuser.id)
    skills = viewuser.skills.split(',')

    projects = Portfolio.select().where(Portfolio.uid == viewuser.id)
    comments = Comment.select()
    services = Service.select().where(Service.uid == viewuser.id)

    return render_template('profile/view.html', user=user, viewuser=viewuser, social_medias=social_medias,
                           followers=followers, following=following, skills=skills, projects=projects,
                           comments=comments, services=services, notifications=notifications)


@profile_bp.route('/follow/<uid>')
@is_auth
def follow(uid):
    user_id = session['user_id']
    user = User.get_by_id(user_id)
    notifications = Notification.select().where(Notification.user == user.id)

    if uid is None:
        flash('User not found', 'error')
        return redirect(url_for('profile.view', id=user_id, notifications=notifications))

    if uid == user_id:
        flash('You cannot follow yourself', 'error')
        return redirect(url_for('profile.view', id=user_id, notifications=notifications))

    viewed_user = User.get_by_id(uid)

    if Follower.get_or_none((Follower.follower_id == user_id) & (Follower.following_id == viewed_user.id))\
            is not None:
        flash('You are already following this user', 'error')
        return redirect(url_for('profile.view', id=user_id, notifications=notifications))

    Follower.create(follower_id=user.id, following_id=viewed_user.id)

    Notification.create(uid=user.id, username=user.username, category='follow', user=viewed_user.id)

    flash('User followed successfully', 'success')
    return redirect(url_for('profile.view', id=user_id, notifications=notifications))


@profile_bp.route('/unfollow/<uid>')
@is_auth
def unfollow(uid):
    user_id = session['user_id']
    user = User.get_by_id(user_id)
    notifications = Notification.select().where(Notification.user == user.id)

    if uid is None:
        flash('User not found', 'error')
        return redirect(url_for('profile.view', id=user_id, notifications=notifications))

    viewed_user = User.get_by_id(uid)

    if Follower.get_or_none((Follower.follower_id == user_id) & (Follower.following_id == viewed_user.id))\
            is None:
        flash('You are not following this user', 'error')
        return redirect(url_for('profile.view', id=user_id, notifications=notifications))

    query = Follower.delete().where((Follower.follower_id == user.id) & (Follower.following_id == viewed_user.id))
    query.execute()

    flash('User unfollowed successfully', 'success')
    return redirect(url_for('profile.view', id=user_id, notifications=notifications))


@profile_bp.route('/profile/edit', methods=['GET', 'POST'])
@is_auth
def edit():
    user_id = session['user_id']
    notifications = Notification.select().where(Notification.user == user_id)

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
    return render_template('profile/edit.html', user=user, social_medias=social_medias, skills=skills,
                           notifications=notifications)


@profile_bp.route('/profile/delete/<id>')
@is_auth
def delete(id):
    user_id = session['user_id']
    notifications = Notification.select().where(Notification.user == user_id)
    if user_id != id:
        flash('You are not authorized to perform this action', 'error')
        return redirect(url_for('profile.view', id=user_id, notifications=notifications))

    query = User.delete().where(User.id == user_id)
    query.execute()

    flash('Account deleted successfully', 'success')
    return redirect(url_for('index.index', notifications=notifications))


@profile_bp.route('/project/add', methods=['GET', 'POST'])
@is_auth
def create_project():
    user_id = session['user_id']
    user = User.get_by_id(user_id)
    notifications = Notification.select().where(Notification.user == user.id)

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
        return redirect(url_for('profile.view', id=user_id, notifications=notifications))

    return render_template('profile/add_project.html', user=user, notifications=notifications)


@profile_bp.route('/project/edit/<id>', methods=['GET', 'POST'])
@is_auth
def edit_project(id):
    user_id = session['user_id']
    user = User.get_by_id(user_id)
    notifications = Notification.select().where(Notification.user == user.id)

    if id is None:
        flash('Project could not be found', 'error')
        return redirect(url_for('profile.view', id=user_id, notifications=notifications))

    project = Portfolio.get_by_id(id)

    if user.id != project.uid:
        flash('You are unauthorized to perform actions on this project', 'error')
        return redirect(url_for('profile.view', id=user_id, notifications=notifications))

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

    return render_template('profile/edit_project.html', user=user, project=project, notifications=notifications)


@profile_bp.route('/project/delete/<id>')
@is_auth
def delete_project(id):
    user_id = session['user_id']
    notifications = Notification.select().where(Notification.user == user_id)

    if id is None:
        flash('Please select a project to delete', 'error')
        return redirect(url_for('profile.view', id=user_id, notifications=notifications))

    project = Portfolio.get_by_id(id)
    if user_id != project.uid:
        flash('You are unauthorized to perform actions on this project', 'error')
        return redirect(url_for('profile.view', id=user_id, notifications=notifications))

    query = Portfolio.delete().where(Portfolio.id == id)
    query.execute()

    flash('Project deleted successfully', 'success')
    return redirect(url_for('profile.view', id=user_id, notifications=notifications))


@profile_bp.route('/project/comment/<vid>/<pid>/<uid>', methods=['POST'])
@is_auth
def comment(vid, pid, uid):
    user = User.get_by_id(uid)
    portfolio = Portfolio.get_by_id(pid)
    viewed = User.get_by_id(vid)
    notifications = Notification.select().where(Notification.user == user.id)

    Comment.create(uid=uid, username=user.username, content=request.form.get('comment'), pid=pid)
    query = Portfolio.update(comments=portfolio.comments + 1).where(Portfolio.id == pid)
    query.execute()
    Notification.create(uid=vid, username=viewed.username, pid=pid, title=portfolio.title,
                        category='comment', user=uid)

    flash('Comment added', 'success')
    return redirect(url_for('profile.view', id=uid, notifications=notifications))
