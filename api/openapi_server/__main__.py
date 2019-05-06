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
        os.getenv('NGS_BITS_DATA', os.getcwd()))
    app.app.config['ALLOWED_EXTENSIONS'] = {'tsv', 'gsvar'}
    origins = os.getenv('CORS_ORIGINS', os.getenv(
        'ORIGINS', ['http://localhost:8080']))
    # enable CORS for all
    CORS(app.app, origins=origins, supports_credentials=True)

    production = os.getenv('PRODUCTION', False)
    if not production:
        @app.app.route('/')
        def serve_index():
            return send_from_directory(directory=os.path.join(os.getcwd(), 'dist'), filename='index.html')

        @app.app.route('/<path:path>')
        def serve_dist(path):
            return send_from_directory(directory=os.path.join(os.getcwd(), 'dist'), filename=path)

    app.run(port=os.getenv('PORT', 9000), debug=not production, use_debugger=not production,
            use_reloader=not production, passthrough_errors=not production)


if __name__ == '__main__':
    main()
