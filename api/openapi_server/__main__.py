#!/usr/bin/env python3

import os

import connexion

from openapi_server import encoder
from flask import send_from_directory
from flask_cors import CORS


def main():
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml', arguments={'title': 'ngs-bits'})
    app.app.config['UPLOAD_FOLDER'] = os.path.abspath(
        os.getenv('DATA', os.getcwd()))
    app.app.config['PRODUCTION'] = os.getenv('PRODUCTION', False)
    app.app.config['ALLOWED_EXTENSIONS'] = {'tsv', 'GSvar'}
    origins = [app.app.host_url]
    origins += os.getenv('CORS_ORIGINS', [])
    # enable CORS for all
    CORS(app.app, origins=origins, supports_credentials=True)

    if not app.app.config['PRODUCTION']:
        @app.app.route('/')
        def serve_index():
            return send_from_directory(directory=os.path.join(os.getcwd(), 'dist'), filename='index.html')

        @app.app.route('/<path:path>')
        def serve_dist(path):
            return send_from_directory(directory=os.path.join(os.getcwd(), 'dist'), filename=path)

    app.run(port=os.getenv('PORT', 9000), debug=not app.app.config['PRODUCTION'], use_debugger=not app.app.config['PRODUCTION'],
            use_reloader=not app.app.config['PRODUCTION'], passthrough_errors=not app.app.config['PRODUCTION'])


if __name__ == '__main__':
    main()
