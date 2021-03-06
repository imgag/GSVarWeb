# coding: utf-8

from __future__ import absolute_import
import unittest

from six import BytesIO

from openapi_server.test import BaseTestCase


class TestFilesController(BaseTestCase):
    """FilesController integration test stubs"""

    def test_count_file_path_get(self):
        """Test case for count_file_path_get


        """
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer abc'
        }
        response = self.client.open(
            '/v1/count/{}'.format('.travis.yml'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_download_file_path_get(self):
        """Test case for download_file_path_get


        """
        headers = {
            'Accept': 'text/gsvar',
            'Lines': '1-100',
            'Authorization': 'Bearer abc'
        }
        response = self.client.open(
            '/v1/download/{}'.format('.travis.yml'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @unittest.skip("multipart/form-data not supported by Connexion")
    def test_upload_post(self):
        """Test case for upload_post


        """
        headers = {
            'Accept': '*/*',
            'Content-Type': 'multipart/form-data',
            'Authorization': 'Bearer abc'
        }
        data = dict(uploaded_file=(BytesIO(b'some file data'), 'file.txt'))
        response = self.client.open(
            '/v1/upload',
            method='POST',
            headers=headers,
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
