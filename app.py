# Copyright (c) 2019 AT&T Intellectual Property. All rights reserved.

# Relative local & stdlib
# config.py is gitignored by convention, so make sure you have your own copy locally.
from config import AAF_SERVICE_REALM, AAF_SERVICE_AUTH, AAF_ROOT_URI
import json
import os

# Frida
from frida.controller.factory import ControllerFactory
import frida.database as fdb
from frida import VALID_MODES

# flask_aaf
from flask_aaf.aaf import Aaf
from flask_aaf.decorators import basic_auth_req
from flask_aaf.util import auth_reject

# Flask
# Blueprint adds /health/ and /ready/ routes
from flask import Flask, request, abort
from base_ms_blueprint import base_ms

app = Flask(__name__)
app.register_blueprint(base_ms)

# AAF_SERVICE_AUTH is a tuple of (username, password) - unpack it
aaf = Aaf(*AAF_SERVICE_AUTH, AAF_SERVICE_REALM, AAF_ROOT_URI)


@app.route('/')
def index():
    return "<h1> Hello, I'm Frida! </h1>"


@app.route('/data360/')
@basic_auth_req
def secret():
    if aaf.has_role('com.att.dplr.nextgen.member'):
        return "<h1> Hi - you're a Data360 member! </h1>"
    else:
        return auth_reject(realm='com.att.dplr.nextgen.member')


@app.route('/modes/')
def get_modes():
    """
    Returns the list of valid modes to operate a Profiler in
    """
    return json.dumps(VALID_MODES)


# TODO: POST only, needs 'callback route' to return post, and/or local mode
@app.route('/profile/', methods=['POST'])
def profile():

    # TODO Add mode and out_loc params, alter RETURN behavior depending on mode, check outloc etc.
    # TODO handle posted files

    try:
        # Requires client to set "Content-Type: application/json"
        if request.get_json() is None:
            abort(400)
        database = fdb.Database(**request.get_json())

    except KeyError:
        # Bad Request
        abort(400)

    controller = ControllerFactory.get_controller(database)
    print("Starting inspection: ")
    print("{0}\t{1}".format(database.host, database.tech_type))

    metadata = controller.profile(database)
    
    print("Inspection complete!")
    return metadata


if __name__ == "__main__":
    _host = os.environ.get('HOST') if os.environ.get('HOST') else '127.0.0.1'
    app.run(host=_host)
