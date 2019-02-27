# Copyright (c) 2019 AT&T Intellectual Property. All rights reserved.

import http

def auth_reject(realm=None):
    """
    Returns a HTTP 401 UNAUTHORIZED response to a user that is being rejected from requesting a resource.

    Use the realm param to control which realm is provided in the rejection
    """
    auth_header_value = 'Basic'
    if realm is not None:
        auth_header_value = auth_header_value + ' realm={realm}'.format(realm=realm)
    
    return ('', http.HTTPStatus.UNAUTHORIZED, {'WWW-Authenticate': auth_header_value})