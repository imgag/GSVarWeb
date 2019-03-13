import os
import tempfile
import uuid

from flask import current_app, abort
from werkzeug.exceptions import BadRequest
import connexion
import six

from openapi_server.models.variant_filter_request import VariantFilterRequest  # noqa: E501
from openapi_server import util
from openapi_server.tools.import_and_convert import convert_dict_to_lines

def variant_filter_annotations_post(variant_filter_request=None):  # noqa: E501
    """variant_filter_annotations_post

     # noqa: E501

    :param variant_filter_request: 
    :type variant_filter_request: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        variant_filter_request = VariantFilterRequest.from_dict(connexion.request.get_json())  # noqa: E501

    absInPath = os.path.join(current_app.config['UPLOAD_FOLDER'], variant_filter_request._in)
    absOutPath = os.path.join(current_app.config['UPLOAD_FOLDER'], variant_filter_request.out)

    if os.path.isfile(absInPath) and not os.path.isfile(absOutPath):
        lines = convert_dict_to_lines(variant_filter_request.filter)
        tmpPath = os.path.join(tempfile.gettempdir(), uuid.uuid4().hex)
        with open(tmpPath, "w") as tmpFile: # write filters file
            tmpFile.write(lines)

        # Run VariantFilterAnnotations
        binFolder = os.path.abspath(os.getenv('NGS_BITS_BIN', os.getcwd()))
        command = "./VariantFilterAnnotations -in {} -out {} -filters {}".format(absInPath, absOutPath, tmpFile.name)
        fullCommand = "cd {} && {}".format(binFolder, command)
        current_app.logger.info("Running {}".format(fullCommand))

        status = os.system(fullCommand)
        if status == 0:
            return "successfull"
        else:
            raise BadRequest("Command exited with status {}".format(status))

        raise BadRequest("Could not create the filter file")
    else:
        raise BadRequest("The file {} wasn't found.".format(body._in))
