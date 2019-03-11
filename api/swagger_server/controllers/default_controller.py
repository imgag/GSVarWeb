import os
import tempfile
import uuid

from flask import current_app, send_from_directory, abort
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest
import connexion
import six

from swagger_server import util

ALLOWED_EXTENSIONS = set(['GSvar'])

def download_file_path_get(filePath):  # noqa: E501
    """download_file_path_get

     # noqa: E501

    :param filePath: Path to the file
    :type filePath: str

    :rtype: file
    """
    absFilePath = os.path.join(current_app.config['UPLOAD_FOLDER'], filePath)
    if os.path.isfile(absFilePath): # this makes sure the upload folder is not escaped
        lines = connexion.request.headers['Lines'] if 'lines' in connexion.request.headers else None
        lines = lines.split('-')

        if lines:
            if len(lines) != 2:
                raise BadRequest("Lines should contain two elements, not {}".format(len(lines)))
            elif lines[0] > lines[1]:
                raise BadRequest("Lines should be formatted like start-end")
            elif int(lines[0]) < 1:
                raise BadRequest("Line start cannot be smaller than one")

            # lines[1] > file_length is handled by sed quite elegantly)
            tmpFile = uuid.uuid4().hex
            tmpPath = os.path.join(tempfile.gettempdir(), tmpFile)
            status = os.system("sed -n '{},{} p' {} >> {}".format(lines[0], lines[1], absFilePath, tmpPath))
            if status == 0:
                return send_from_directory(directory=tempfile.gettempdir(), filename=tmpFile)
            else:
                raise BadRequest("Command exited with status {}".format(status))
        else:
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
