import os

from flask import current_app, abort
from werkzeug.exceptions import BadRequest


def an_vep_file_path_get(filePath, user=None):  # noqa: E501
    """an_vep_file_path_get

    Annotates a VCF using VEP # noqa: E501

    :param file_path: The VCF file to annotate
    :type file_path: str
    :param user: The user name.
    :type user: str.

    :rtype: string
    """
    abs_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], user, filePath)
    if os.path.isfile(abs_file_path):
        abs_out_path = abs_file_path.replace(".vcf", "_annotated.vcf")
        meg_sap = os.path.abspath(os.getenv('MEGSAP', ""))
        meg_sap_command = "php {}/src/NGS/an_vep.php -in {} -out {}".format(
            meg_sap, abs_file_path, abs_out_path)
        status = os.system(meg_sap_command)
        if status == 0:
            return os.path.basename(abs_out_path)
        else:
            raise BadRequest(
                "Command exited with status {}".format(status))
        return os.path.basename(abs_out_path)
    else:
        abort(404)


def vcf2gsvar_file_path_get(filePath, user=None):  # noqa: E501
    """vcf2gsvar_file_path_get

    Converts a VCF file to a GSvar # noqa: E501

    :param file_path: The GSvar file to convert
    :type file_path: str
    :param user: The user name.
    :type user: str.

    :rtype: string
    """
    abs_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], user, filePath)
    if os.path.isfile(abs_file_path):
        abs_gsvar_path = abs_file_path.replace(".vcf", ".GSvar")
        meg_sap = os.path.abspath(os.getenv("MEGSAP", ""))
        meg_sap_command = "php {}/src/NGS/vcf2gsvar.php -in {} -out {}".format(
            meg_sap, abs_file_path, abs_gsvar_path)
        status = os.system(meg_sap_command)
        if status == 0:
            return os.path.basename(abs_gsvar_path)
        else:
            raise BadRequest(
                "Command failed while producing a GSvar file with status {}".format(status))
        return os.path.basename(abs_gsvar_path)
    else:
        abort(404)
