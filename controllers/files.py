import config.constants
import magic
import os
import re
from flask import Blueprint, render_template, request, url_for, redirect, flash, session, send_from_directory
from pathlib import Path
from playhouse.shortcuts import *
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
    user_files = File.select().where(File.uid == user_id)
    files = []
    share = {'uids': [], 'usernames': [], 'emails': []}

    user_files = [model_to_dict(file) for file in user_files]

    for file in user_files:
        share_uids = file['shareUid'].split(',')
        for share_uid in share_uids:
            share_users = User.select().where(User.id in share_uid.split(','))
            for share_user in share_users:
                share_user = model_to_dict(share_user)

                share['uids'].append(str(share_user['id']))
                share['usernames'].append(share_user['username'])
                share['emails'].append(share_user['email'])
                file['share'] = share

                size = round(os.path.getsize(file['fullPath'])/1000, 2)
                file['size'] = str(size) + ' kb'
                if size >= 1000:
                    file['size'] = str(round(size/1000, 2)) + ' mb'

                files.append(file)

    return render_template('files/index.html', user=user, files=files)


@files_bp.route('/upload', methods=['POST'])
@is_auth
def upload_file():
    user_id = session.get('user_id')
    files = request.files.getlist('poster')

    directory = config.constants.uploads_dir + '/' + str(user_id) + '/files/'

    for file in files:
        full_path = os.path.join(directory, file.filename)
        Path(directory).mkdir(exist_ok=True)
        if os.path.exists(full_path):
            os.remove(full_path)

        file.save(full_path)
        file_type = mime.from_file(full_path)
        file_type = file_type[file_type.index('/') + 1:]
        size = os.path.getsize(full_path)
        if size/1000000 >= 100:
            flash('File cannot exceed 100mb in size', 'error')

        File.create(name=file.filename[:file.filename.index('.')], type=file_type, uid=user_id,
                    directory=directory, fullPath=full_path)

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
    unshare_user = req.getlist('uid')

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

        file = File.get_by_id(fid)
        os.rename(file.fullPath, file.directory + name + '.' + file.type)
        query = File.update(name=name).where(File.id == fid)
        query.execute()

        flash('File or folder renamed successfully', 'success')

    else:
        flash('No file or folder selected', 'error')

    return redirect(url_for('files.manage'))


@files_bp.route('/download/<fid>', methods=['POST'])
@is_auth
def download(fid):
    if fid:
        user_id = session['user_id']
        file = File.get_by_id(fid)
        share_uids = file.shareUid.split(',')

        if user_id not in share_uids and user_id != file.uid:
            flash('You do not have permission to download this file', 'error')

        else:
            return send_from_directory(directory=file.directory, filename=file.name + '.' + file.type)

    else:
        flash('You do not have permission to download this file/This file can\'t be found', 'error')

    return redirect(url_for('files.manage'))
