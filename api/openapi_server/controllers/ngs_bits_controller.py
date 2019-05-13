import os
import tempfile
import uuid

from flask import current_app, abort
from werkzeug.exceptions import BadRequest
import connexion

from openapi_server.models.variant_filter_request import VariantFilterRequest  # noqa: E501
from openapi_server.tools.import_and_convert import convert_dict_to_lines


def variant_filter_annotations_post(variant_filter_request=None):  # noqa: E501
    """variant_filter_annotations_post

    :param variant_filter_request:
    :type variant_filter_request: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        variant_filter_request = VariantFilterRequest.from_dict(connexion.request.get_json())  # noqa: E501

    abs_in_path = os.path.join(
        current_app.config['UPLOAD_FOLDER'], variant_filter_request._in)
    abs_out_path = os.path.join(
        current_app.config['UPLOAD_FOLDER'], variant_filter_request.out)

    if os.path.isfile(abs_in_path) and not os.path.isfile(abs_out_path):
        lines = convert_dict_to_lines(variant_filter_request.filter)
        tmp_path = os.path.join(tempfile.gettempdir(), uuid.uuid4().hex)
        with open(tmp_path, "w") as tmpFile:  # write filters file
            tmpFile.write(lines)

        # Run VariantFilterAnnotations
        bin_folder = os.path.abspath(os.getenv('NGS_BITS_BIN', os.getcwd()))
        command = "./VariantFilterAnnotations -in {} -out {} -filters {}".format(
            abs_in_path, abs_out_path, tmpFile.name)
        full_command = "cd {} && {}".format(bin_folder, command)
        current_app.logger.info("Running {}".format(full_command))

        status = os.system(full_command)
        if status == 0:
            return "successfull"
        else:
            raise BadRequest("Command exited with status {}".format(status))
    else:
        raise BadRequest("The file {} wasn't found.".format(
            variant_filter_request._in))


def vcf_check_file_path_get(filePath):  # noqa: E501
    """vcf_check_file_path_get
    Check a file at given path with VcfCheck.

    :param filePath: Path to the file
    :type filePath: str

    :rtype: None
    """

    abs_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filePath)
    if os.path.isfile(abs_file_path):

        bin_folder = os.path.abspath(os.getenv('NGS_BITS_BIN', os.getcwd()))
        command = "./VcfCheck -in {}".format(abs_file_path)
        full_command = "cd {} && {}".format(bin_folder, command)
        current_app.logger.info("Running {}".format(full_command))
        status = os.system(full_command)
        if status == 0:
            return "successfull"
        else:
            raise BadRequest("Command exited with status {}".format(status))
    else:
        abort(404)

    return None
