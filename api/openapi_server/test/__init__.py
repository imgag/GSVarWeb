import os
import logging

import connexion
from flask_testing import TestCase

from openapi_server.encoder import JSONEncoder


class BaseTestCase(TestCase):

    def create_app(self):
        logging.getLogger('connexion.operation').setLevel('ERROR')
        app = connexion.App(__name__, specification_dir='../openapi/')
        app.app.config['UPLOAD_FOLDER'] = os.path.abspath(
            os.getenv('NGS_BITS_DATA', os.getcwd()))
        app.app.json_encoder = JSONEncoder
        app.add_api('openapi.yaml')
        return app.app
