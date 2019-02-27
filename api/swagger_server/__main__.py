#!/usr/bin/env python3

import os

import connexion

from swagger_server import encoder


def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'ngs-bits'})
    app.app.config['UPLOAD_FOLDER'] = os.path.abspath(os.getenv('NGS_BITS_DATA', os.getcwd()))
    app.app.config['ALLOWED_EXTENSIONS'] = set(['tsv', 'gsvar'])
    app.run(port=8080)


if __name__ == '__main__':
    main()
