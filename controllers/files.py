import shutil
import config.constants
import magic
import os
import re
import ast
from flask import Blueprint, render_template, request, url_for, redirect, flash, session, send_from_directory
from pathlib import Path
from urllib.parse import unquote
from playhouse.shortcuts import *
from middlewares.auth import is_auth
from models.user import User
from models.filesFolders import File
from models.notifications import Notification


files_bp = Blueprint('files', __name__, template_folder=config.constants.template_dir,
                     static_folder=config.constants.static_dir, static_url_path='public', url_prefix='/files')
mime = magic.Magic(mime=True)


@files_bp.route('/manage', methods=['GET', 'POST'])
@is_auth
def manage():
    if request.get_json() is not None and request.method == 'POST':
        return redirect(url_for('files.delete', selected_ids=request.get_json()))

    user_id = session.get('user_id')
    user = User.get_by_id(user_id)
    notifications = Notification.select().where(Notification.user == user.id)
    files = []
    share = {'uids': [], 'usernames': [], 'emails': []}

    file_path = request.args.get('path')
    breadcrumbs = [{'name': 'My Drive'}]

    root = config.constants.uploads_dir + '/' + str(user_id) + '/files/'

    Path(root).mkdir(exist_ok=True)
    user_dir_items = [os.path.splitext(file_name)[0] for file_name in os.listdir(root)]
    user_files = File.select().where((File.uid == user_id) & (File.name << user_dir_items))

    user_files = [model_to_dict(file) for file in user_files]

    if file_path is not None:
        links = file_path.split(',')
        full_link = ''
        breadcrumbs[0]['link'] = '/files/manage'
        for link in links:
            full_link += link + ','
            print(full_link)
            breadcrumbs.append({'name': link, 'link': '/files/manage?path=' + full_link})

        user_files.clear()
        selected = os.listdir(root + file_path.replace(',', '/'))

        for item in selected:
            item = item[:item.index('.')] if '.' in item else item

            file = File.get(File.name == item)
            file = model_to_dict(file)
            user_files.append(file)

    for file in user_files:
        share_uids = file['shareUid'].split(',')

        for share_uid in share_uids:
            share_users = User.select().where(User.id << share_uid.split(','))
            if share_users:
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

            if file['type'] == 'folder':
                file['link'] = '/files/manage?path=' + file['fullPath'][file['fullPath'].index('files/') + 6:]\
                    .replace('\\', ',').replace('/', ',')

            files.append(file)

    return render_template('files/index.html', user=user, files=files, breadcrumbs=breadcrumbs,
                           notifications=notifications)


@files_bp.route('/upload', methods=['POST'])
@is_auth
def upload_file():
    user_id = session.get('user_id')
    files = request.files.getlist('poster')

    directory = config.constants.uploads_dir + '/' + str(user_id) + '/files/'

    for file in files:
        url = request.referrer

        full_path = os.path.join(directory, file.filename) if len(url.split('=')) == 1 else \
            os.path.join(directory, unquote(url.split('=')[1]).replace(',', '/'), file.filename)

        Path(directory).mkdir(exist_ok=True)
        if os.path.exists(full_path) and len(url.split('=')) == 1:
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


@files_bp.route('/delete')
@is_auth
def delete():
    selected_ids = request.args.get('selected_ids')
    selected_ids = ast.literal_eval(selected_ids)

    for id in selected_ids.values():
        file = File.get_or_none(id)

        if file is None:    # TODO: Figure out why toast not showing
            flash('File/Folder could not be found', 'error')
            return redirect(url_for('files.manage'))
        shutil.rmtree(file.fullPath) if file.type == 'folder' else os.remove(file.fullPath)

        query = File.delete().where(File.id == id)
        query.execute()

    flash('File/Folder(s) deleted successfully', 'success')
    return redirect(url_for('files.manage'))


@files_bp.route('/share', methods=['POST'])
@is_auth
def share():
    req = request.form
    fid = req.get('fid')
    share_user = req.get('shareUser')
    user_id = session.get('user_id')
    user = User.get_by_id(user_id)

    if fid is not None:
        file = File.get_by_id(fid)
        share_user = User.select().where((User.username == share_user) | (User.email == share_user))
        share_username = share_user[0].username
        share_id = share_user[0].id
        share_list = file.shareUid.split(',').append(share_user[0].id)
        share_user = ",".join(share_list)

        query = File.update(shareUid=share_user).where(File.id == fid)
        query.execute()

        Notification.create(uid=int(user_id), username=user.username, title=file.name, category='file_share',
                            user=share_id)

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
    user_id = session.get('user_id')
    user = User.get_by_id(user_id)

    if fid is not None:
        file = File.get_by_id(fid)
        share_list = file.shareUid.split(',')

        for unshare_user_id in unshare_user:
            share_list.remove(unshare_user_id)
            Notification.create(uid=int(user_id), username=user.username, title=file.name, category='file_unshare',
                                user=unshare_user_id)

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
    if fid is not None:
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
    if fid is not None:
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


@files_bp.route('/create-folder', methods=['POST'])
@is_auth
def create_folder():
    user_id = session['user_id']
    name = request.form.get('name')
    regex = re.compile(r'/[!@#$%^&*+\=\[\]{}()~;:"\\|,.<>\/?]/')
    root = config.constants.uploads_dir + '/' + str(user_id) + '/files/'

    if name is not None:
        flash('Folder name can\'t be empty', 'error')

    if re.match(regex, name):
        flash('File or folder name only allow alphanumeric, underscore and dash', 'error')

    url = request.referrer
    full_path = os.path.join(root, name) if len(url.split('=')) == 1 else \
        os.path.join(root, unquote(url.split('=')[1]).replace(',', '/'), name)

    if os.path.exists(full_path):
        flash('Folder already exists in current directory', 'error')

    else:
        os.mkdir(full_path)
        File.create(name=name, directory=root, fullPath=full_path, type='folder', uid=user_id)

    flash('Folder created successfully', 'success')
    return redirect(url_for('files.manage'))
