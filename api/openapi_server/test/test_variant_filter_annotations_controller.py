# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from openapi_server.models.variant_filter_request import VariantFilterRequest  # noqa: E501
from openapi_server.test import BaseTestCase


class TestVariantFilterAnnotationsController(BaseTestCase):
    """VariantFilterAnnotationsController integration test stubs"""

    def test_variant_filter_annotations_post(self):
        """Test case for variant_filter_annotations_post

        
        """
        variant_filter_request = VariantFilterRequest()
        response = self.client.open(
            '/v1/VariantFilterAnnotations',
            method='POST',
            data=json.dumps(variant_filter_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
