# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from openapi_server.test import BaseTestCase


class TestMegSAPController(BaseTestCase):
    """MegSAPController integration test stubs"""

    def test_vcf2gsvar_file_path_get(self):
        """Test case for vcf2gsvar_file_path_get

        
        """
        response = self.client.open(
            '/v1/vcf2gsvar/{filePath}'.format(file_path='file_path_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
