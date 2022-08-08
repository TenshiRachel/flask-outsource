import config.constants
from flask import Blueprint, render_template, request, url_for, redirect, flash, session
from middlewares.auth import is_auth
from models.user import User
from models.notifications import Notification

notifications_bp = Blueprint('notifications', __name__, template_folder=config.constants.template_dir,
                             static_folder=config.constants.static_dir, static_url_path='public',
                             url_prefix='/notifications')


@notifications_bp.route('/')
@is_auth
def index():
    user_id = session.get('user_id')
    user = User.get_by_id(user_id)

    like_notifications = Notification.select().where((Notification.user == user_id) & (Notification.category == 'likes'))\
        .order_by(Notification.date.desc())

    followers_notifications = Notification.select().where((Notification.user == user_id) & (Notification.category == 'follow'))\
        .order_by(Notification.date.desc())

    comment_notifications = Notification.select().where((Notification.user == user_id) & (Notification.category == 'comment'))\
        .order_by(Notification.date.desc())

    job_reject_notifications = Notification.select().\
        where((Notification.user == user_id) & (Notification.category == 'job_reject')).order_by(Notification.date.desc())

    job_notifications = Notification.select().\
        where((Notification.user == user_id) & (Notification.category == 'job')).order_by(Notification.date.desc())

    paid_jobs_notifications = Notification.select().\
        where((Notification.user == user_id) & (Notification.category == 'job_paid')).order_by(Notification.date.desc())

    request_cancelled_notifications = Notification.select().\
        where((Notification.user == user_id) & (Notification.category == 'request_cancel'))\
        .order_by(Notification.date.desc())

    complete_requests_notifications = Notification.select().\
        where((Notification.user == user_id) & (Notification.category == 'request_complete'))\
        .order_by(Notification.date.desc())

    file_share_notifications = Notification.select().\
        where((Notification.user == user_id) & (Notification.category == 'file_share')).order_by(Notification.date.desc())

    file_unshare_notifications = Notification.select().\
        where((Notification.user == user_id) & (Notification.category == 'file_unshare')).order_by(Notification.date.desc())

    return render_template('notifications/index.html', user=user, like_notifications=like_notifications,
                           followers_notifications=followers_notifications, comment_notifications=comment_notifications,
                           job_reject_notifications=job_reject_notifications, job_notifications=job_notifications,
                           request_cancelled_notifications=request_cancelled_notifications,
                           file_share_notifications=file_share_notifications,
                           file_unshare_notifications=file_unshare_notifications,
                           complete_requests_notifications=complete_requests_notifications,
                           paid_jobs_notifications=paid_jobs_notifications)


@notifications_bp.route('/delete/<id>')
@is_auth
def delete(id):
    if Notification.get_or_none(Notification.id == id) is None:
        flash('Notification could not be found', 'error')
        return redirect(url_for('notifications.index'))

    query = Notification.delete().where(Notification.id == id)
    query.execute()

    flash('Notification deleted successfully', 'success')
    return redirect(url_for('notifications.index'))


@notifications_bp.route('/deleteAll/<category>')
@is_auth
def delete_all(category):
    user_id = session['user_id']
    count = len(Notification.select().where((Notification.user == user_id) & (Notification.category == category)))

    if count <= 0:
        flash('Notifications could not be found', 'error')
        return redirect(url_for('notifications.index'))

    query = Notification.delete().where((Notification.user == user_id) & (Notification.category == category))
    query.execute()

    flash('Notification(s) deleted successfully', 'success')
    return redirect(url_for('notifications.index'))
