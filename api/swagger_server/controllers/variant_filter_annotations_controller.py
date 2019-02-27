import connexion
import six

from swagger_server.models.variant_filter_request import VariantFilterRequest  # noqa: E501
from swagger_server import util


def variant_filter_annotations_post(body=None):  # noqa: E501
    """variant_filter_annotations_post

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = VariantFilterRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
