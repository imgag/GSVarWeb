import os

from flask import current_app, send_from_directory, abort
from werkzeug.utils import secure_filename
import connexion
import six

from swagger_server import util

ALLOWED_EXTENSIONS = set(['GSvar'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def download_file_path_get(filePath):  # noqa: E501
    """download_file_path_get

     # noqa: E501

    :param filePath: Path to the file
    :type filePath: str

    :rtype: file
    """
    absFilePath = os.path.join(current_app.config['UPLOAD_FOLDER'], filePath)
    if os.path.isfile(absFilePath): # this makes sure the upload folder is not escaped
        return send_from_directory(directory=current_app.config['UPLOAD_FOLDER'], filename=filePath)
    else:
        abort(404)

def upload_post(uploadedFile=None):  # noqa: E501
    """upload_post

    Uploads a file to the server # noqa: E501

    :param uploadedFile: The GSVar file to upload.
    :type uploadedFile: werkzeug.datastructures.FileStorage

    :rtype: None
    """
    fileName = secure_filename(uploadedFile.filename)
    absFilePath = os.path.join(current_app.config['UPLOAD_FOLDER'], fileName)
    if os.path.exists(absFilePath):
        pass
    else:
        uploadedFile.save(absFilePath) # this will raise a IOError if something goes wrong

    return "successfull"
