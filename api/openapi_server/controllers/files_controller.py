import os
import tempfile
import uuid
import subprocess
from locale import getpreferredencoding

from flask import current_app, send_from_directory, abort
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest
import connexion


ALLOWED_EXTENSIONS = set('GSvar')


def count_file_path_get(filePath, user=None):  # noqa: E501
    """count_file_path_get

    Count items in a file # noqa: E501

    :param filePath: Path to the file
    :type filePath: str

    :rtype: float
    """
    user_dir = user if user else 'debug'
    abs_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], user_dir, filePath)
    if current_app.config['PRODUCTION']:
        if not any(map(lambda extension: filePath.endswith(extension), current_app.config['ALLOWED_EXTENSIONS'])):
            return "File must be one of allowed types.", 400

    if os.path.isfile(abs_file_path):
        command = "cat {} | grep -v '#' | wc -l".format(abs_file_path)
        count = subprocess.check_output(command, shell=True)
        count = str(count, getpreferredencoding()).strip()
        return count
    else:
        abort(404)


def download_file_path_get(filePath, user=None):  # noqa: E501
    """download_file_path_get

    Download a file from given path eventually cutting it with Lines header # noqa: E501

    :param filePath: Path to the file
    :type filePath: str
    :param user: The user name.
    :type user: str

    :rtype: file
    """

    if current_app.config['PRODUCTION']:
        if not any(map(lambda extension: filePath.endswith(extension), current_app.config['ALLOWED_EXTENSIONS'])):
            return "File must be one of allowed types.", 400
    user_dir = user if user else 'debug'
    abs_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], user_dir, filePath)
    if os.path.isfile(abs_file_path):  # this makes sure the upload folder is not escaped
        lines = connexion.request.headers['Lines'] if 'lines' in connexion.request.headers else None

        if lines:
            lines = lines.split('-')
            if len(lines) != 2:
                raise BadRequest(
                    "Lines should contain two elements, not {}".format(len(lines)))
            elif not len(lines[0]):
                raise BadRequest("You cannot specify a negative number here..")
            elif lines[0] > lines[1]:
                raise BadRequest("Lines should be formatted like start-end")
            elif int(lines[0]) < 1:
                raise BadRequest("Line start cannot be smaller than one")

            # lines[1] > file_length is handled by sed quite elegantly)
            tmp_file = uuid.uuid4().hex
            tmp_path = os.path.join(tempfile.gettempdir(), tmp_file)
            status = os.system(
                "sed -n '{},{} p' {} >> {}".format(lines[0], lines[1], abs_file_path, tmp_path))
            if status == 0:
                return send_from_directory(directory=tempfile.gettempdir(), filename=tmp_file)
            else:
                raise BadRequest(
                    "Command exited with status {}".format(status))
        else:
            return send_from_directory(directory=current_app.config['UPLOAD_FOLDER'], filename=filePath)
    else:
        abort(404)
    return 'do some magic!'


def upload_post(uploadedFile=None, user=None):  # noqa: E501
    """upload_post

    Uploads a file to the server # noqa: E501

    :param uploadedFile: The GSVar file to upload.
    :type uploadedFile: werkzeug.datastructures.FileStorage
    :param user: The user name.
    :type user: str.

    :rtype: None
    """
    user_dir = user if user else 'debug'
    file_name = secure_filename(uploadedFile.filename)
    if current_app.config['PRODUCTION']:
        if not any(map(lambda extension: file_name.endswith(extension), current_app.config['ALLOWED_EXTENSIONS'])):
            return "File must be one of allowed types.", 400
    abs_folder_path = os.path.join(
        current_app.config['UPLOAD_FOLDER'],
        user_dir
    )
    abs_file_path = os.path.join(
        abs_folder_path,
        file_name
    )
    if not os.path.exists(abs_folder_path):
        os.mkdir(abs_folder_path)
    if os.path.exists(abs_file_path):
        pass
    else:
        # this will raise a IOError if something goes wrong
        uploadedFile.save(abs_file_path)

    return "successfull"
