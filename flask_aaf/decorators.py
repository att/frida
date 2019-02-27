# Copyright (c) 2019 AT&T Intellectual Property. All rights reserved.

from functools import wraps
from flask_aaf.util import auth_reject
import flask

def basic_auth_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if flask.request.authorization is None:
           return auth_reject()
        return f(*args, **kwargs)
    return decorated_function

# Use as an example for decorators with params
def basic_auth_req_option(active=False):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if active:
                if flask.request.authorization is None:
                    return auth_reject()
            return f(*args, **kwargs)
        return decorated_function
    return decorator