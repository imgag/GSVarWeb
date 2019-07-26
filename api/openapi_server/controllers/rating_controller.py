import connexion
import six

from openapi_server import util


def annotated_file_path_get(file_path):  # noqa: E501
    """annotated_file_path_get

    Retrieves an annotated version of the file. # noqa: E501

    :param file_path: Path to file
    :type file_path: str

    :rtype: None
    """
    return 'do some magic!'


def rate_file_path_chr_start_end_rating_put(file_path, chr, start, end, rating):  # noqa: E501
    """rate_file_path_chr_start_end_rating_put

    Rate a file. This uses JWT to verify the user. # noqa: E501

    :param file_path: Path to file
    :type file_path: str
    :param chr: The chromosome to rate for
    :type chr: str
    :param start: The start position to rate for
    :type start: 
    :param end: The end position to annotate for
    :type end: 
    :param rating: Which rating this variant should have.
    :type rating: 

    :rtype: None
    """
    return 'do some magic!'
