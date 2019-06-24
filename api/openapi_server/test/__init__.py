import logging
import os

import connexion
from flask_testing import TestCase

from openapi_server.encoder import JSONEncoder


class BaseTestCase(TestCase):

    def create_app(self):
        logging.getLogger('connexion.operation').setLevel('ERROR')
        app = connexion.App(__name__, specification_dir='../openapi/')
        app.app.json_encoder = JSONEncoder
        app.app.config['PRODUCTION'] = False
        app.app.config['UPLOAD_FOLDER'] = os.path.abspath(
            os.getenv('DATA', os.getcwd())
        )
        app.add_api('openapi.yaml', pythonic_params=False)
        return app.app
