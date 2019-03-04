import os
import tempfile

from flask import current_app, abort
import connexion
import six

from swagger_server.models.variant_filter_request import VariantFilterRequest  # noqa: E501
from swagger_server import util
from swagger_server.tools.import_and_convert import convert_dict_to_lines


def variant_filter_annotations_post(body=None):  # noqa: E501
    """variant_filter_annotations_post

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = VariantFilterRequest.from_dict(connexion.request.get_json())  # noqa: E501
    
    absInPath = os.path.join(current_app.config['UPLOAD_FOLDER'], body._in)
    absOutPath = os.path.join(current_app.config['UPLOAD_FOLDER'], body.out)

    if os.path.isfile(absInPath) and not os.path.isfile(absOutPath):
        lines = convert_dict_to_lines(body.filter)
        with tempfile.NamedTemporaryFile(mode='w') as tmpFile: # Create filters for given JSON
            tmpFile.write(lines)

            # Run VariantFilterAnnotations
            binFolder = os.path.abspath(os.getenv('NGS_BITS_BIN', os.getcwd()))
            command = "./VariantFilterAnnotations -in {} -out {} -filters {}".format(absInPath, absOutPath, tmpFile.name)

            status = os.system("cd {} && {}".format(binFolder, command))
            if status == 0:
                return "successful"
            else:
                abort(400) # TODO: Make this more detailed

        abort(400, message="Could not create the filter file")
    else:
        abort(400, message="The file {} wasn't found.".format(body._in))
