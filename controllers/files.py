import config.constants
import magic
import os
import re
from flask import Blueprint, render_template, request, url_for, redirect, flash, session
from middlewares.auth import is_auth
from models.user import User
from models.filesFolders import File


files_bp = Blueprint('files', __name__, template_folder=config.constants.template_dir,
                     static_folder=config.constants.static_dir, static_url_path='public', url_prefix='/files')
mime = magic.Magic(mime=True)


@files_bp.route('/manage')
@is_auth
def manage():
    user_id = session.get('user_id')
    user = User.get_by_id(user_id)
    files = File.select().where(File.uid == user_id)

    return render_template('files/index.html', user=user, files=files)


@files_bp.route('/upload', methods=['POST'])
@is_auth
def upload_file():
    user_id = session.get('user_id')
    files = request.files.getlist('files')

    directory = config.constants.uploads_dir + '/uploads/' + str(user_id) + '/files/'

    for file in files:
        file_type = mime.from_file(file.filename)
        file_type = file_type[file_type.index('/'):]
        full_path = os.path.join(directory, file.filename)
        File.create(name=file.filename, type=file_type, uid=user_id,
                    directory=directory, fullPath=full_path)

        if os.path.exists(full_path):
            os.remove(full_path)

        file.save(directory + file.filename)

    flash('File(s) uploaded successfully', 'success')
    return redirect(url_for('files.manage'))


@files_bp.route('/share', methods=['POST'])
@is_auth
def share():
    req = request.form
    fid = req.get('fid')
    share_user = req.get('shareUser')

    if fid:
        file = File.get_by_id(fid)
        share_user = User.select().where((User.username == share_user) | (User.email == share_user))
        share_username = share_user[0].username
        share_list = file.shareUid.split(',').append(share_user[0].id)
        share_user = ",".join(share_list)

        query = File.update(shareUid=share_user).where(File.id == fid)
        query.execute()

        flash('Successfully shared with ' + share_username, 'success')

    else:
        flash('No file or folder selected', 'error')

    return redirect(url_for('files.manage'))


@files_bp.route('/unshare', methods=['POST'])
@is_auth
def unshare():
    req = request.form
    fid = req.get('fid')
    unshare_user = req.getlist('shareUser')

    if fid:
        file = File.get_by_id(fid)
        share_list = file.shareUid.split(',')

        for user_id in unshare_user:
            share_list.remove(user_id)

        share_list = ",".join(share_list)

        query = File.update(shareUid=share_list).where(File.id == fid)
        query.execute()

        flash('Unshared successfully', 'success')

    else:
        flash('No file or folder selected', 'error')

    return redirect(url_for('files.manage'))


@files_bp.route('/rename', methods=['POST'])
@is_auth
def rename():
    req = request.form
    fid = req.get('fid')
    name = req.get('rename')
    regex = re.compile(r'/[!@#$%^&*+\=\[\]{}()~;:"\\|,.<>\/?]/')
    if fid:
        if re.match(regex, name):
            flash('File or folder name only allow alphanumeric, space, underscore and dash', 'error')

        query = File.update(name=name).where(File.id == fid)
        query.execute()

        flash('File or folder renamed successfully', 'success')

    else:
        flash('No file or folder selected', 'error')

    return redirect(url_for('files.manage'))
