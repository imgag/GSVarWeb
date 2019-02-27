import os

from flask import current_app, send_from_directory, abort
import connexion
import six

from swagger_server import util


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
