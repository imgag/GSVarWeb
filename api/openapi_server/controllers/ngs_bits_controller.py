import os
import tempfile
import uuid
import subprocess

from flask import current_app, abort
from werkzeug.exceptions import BadRequest
import connexion

from openapi_server.tools.import_and_convert import convert_dict_to_lines


def variant_filter_annotations_post(variant_filter_request=None, user=None):  # noqa: E501
    """variant_filter_annotations_post

    :param variant_filter_request:
    :type variant_filter_request: dict | bytes
    :param user: The user name.
    :type user: str.

    :rtype: None
    """
    if connexion.request.is_json:
        variant_filter_request = connexion.request.get_json()

    abs_in_path = os.path.join(
        current_app.config['UPLOAD_FOLDER'], user, variant_filter_request['in'])
    abs_out_path = os.path.join(
        current_app.config['UPLOAD_FOLDER'], user, variant_filter_request['out'])

    if os.path.isfile(abs_in_path) and not os.path.isfile(abs_out_path):
        lines = convert_dict_to_lines(variant_filter_request['filter'])
        tmp_path = os.path.join(tempfile.gettempdir(), uuid.uuid4().hex)
        with open(tmp_path, "w") as tmpFile:  # write filters file
            tmpFile.write(lines)

        # Run VariantFilterAnnotations
        bin_folder = os.path.abspath(os.getenv('NGS_BITS', os.getcwd()))
        filter_call = subprocess.run([os.path.join(bin_folder, 'VariantFilterAnnotations'), '-in',
                                      abs_in_path, '-out', abs_out_path, '-filters', tmpFile.name],
                                     cwd=bin_folder,
                                     capture_output=True)
        if filter_call.returncode == 0:
            return "successfull"
        else:
            error = filter_call.stderr.decode('utf-8').split('\n')
        raise BadRequest(error[1])
    else:
        raise BadRequest("The file {} wasn't found.".format(
            variant_filter_request['in']))


def vcf_check_file_path_get(filePath, user=None):  # noqa: E501
    """vcf_check_file_path_get
    Check a file at given path with VcfCheck.

    :param filePath: Path to the file
    :type filePath: str
    :param user: The user name.
    :type user: str.

    :rtype: None
    """

    abs_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], user, filePath)
    if os.path.isfile(abs_file_path):

        bin_folder = os.path.abspath(os.getenv('NGS_BITS', os.getcwd()))
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
