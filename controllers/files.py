import config.constants
import magic
import os
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
    user = User.get_by_id(user_id)
    files = request.files.getlist('files')

    directory = config.constants.uploads_dir + '/uploads/' + str(user_id) + '/files/'

    for file in files:
        file_type = mime.from_file(file.filename)
        file_type = file_type[file_type.index('/'):]
        full_path = os.path.join(directory, file.filename)
        new_file = File.create(name=file.filename, type=file_type, uid=user_id,
                               directory=directory, fullPath=full_path)
        file.save(directory + file.filename)

    flash('File(s) uploaded successfully', 'success')
    return redirect(url_for('files.manage'))
