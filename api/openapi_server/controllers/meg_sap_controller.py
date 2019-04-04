import os

import connexion
import six
from flask import current_app, abort
from werkzeug.exceptions import BadRequest

from openapi_server import util

def vcf2gsvar_file_path_get(filePath):  # noqa: E501
    """vcf2gsvar_file_path_get

    Converts a VCF file to a GSvar # noqa: E501

    :param file_path: The GSvar file to convert
    :type file_path: str

    :rtype: None
    """

    absFilePath = os.path.join(current_app.config['UPLOAD_FOLDER'], filePath)
    if os.path.isfile(absFilePath):
        absGSvarPath = absFilePath.replace(".vcf", ".GSvar")
        if not os.path.isfile(absGSvarPath):
            binFolder = os.path.abspath(os.getenv('NGS_BITS_BIN', os.getcwd()))
            command = "./VcfCheck -in {}".format(absFilePath)
            fullCommand = "cd {} && {}".format(binFolder, command)

            status = os.system(fullCommand)
            if status != 0:
                raise BadRequest("Command exited with status while checking the VCF {}".format(status))

            megSAP = os.path.abspath(os.getenv('MEGSAP_DIR'))
            megSAPcommand = "php {}/src/NGS/vcf2gsvar.php -in {} -out {}".format(megSAP, absFilePath, absGSvarPath)
            status = os.system(megSAPcommand)
            if status == 0:
                return os.path.basename(absGSvarPath)
            else:
                raise BadRequest("Command failed while producing a GSvar file with status {}".format(status))
        else:
            return os.path.basename(absGSvarPath)
    else:
        abort(400)
