# Copyright (c) 2019 AT&T Intellectual Property. All rights reserved.

from flask import Blueprint, abort
from http import HTTPStatus

base_ms = Blueprint('base_ms', __name__, static_folder='static')

@base_ms.route('/health/')
def health():
    try:
        # Add additional health checks here
        return ('', HTTPStatus.OK)
    except:
        abort(500)

@base_ms.route('/ready/')
def ready():
    try:
        # Add additional ready checks here
        return ('', HTTPStatus.OK)
    except:
        abort(500)
