# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.variant_filter_request import VariantFilterRequest  # noqa: E501
from openapi_server.test import BaseTestCase


class TestNgsBitsController(BaseTestCase):
    """NgsBitsController integration test stubs"""

    def test_variant_filter_annotations_post(self):
        """Test case for variant_filter_annotations_post

        
        """
        variant_filter_request = {
  "filter" : [ "{}", "{}" ],
  "in" : "in",
  "out" : "out"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/v1/VariantFilterAnnotations',
            method='POST',
            headers=headers,
            data=json.dumps(variant_filter_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
