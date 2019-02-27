# Copyright (c) 2019 AT&T Intellectual Property. All rights reserved.

from functools import wraps
from http import HTTPStatus
import flask
import requests
import json

class Aaf(object):
    """
    Represents the AAF home server
    """
    def __init__(self, service_user, service_password, service_realm, root_uri='https://aaf.it.att.com:8095/proxy'):
        self.root_uri = root_uri
        self.service_user = service_user
        # !!!
        self.service_password = service_password
        self.service_realm = service_realm

        # Validate service credentials
        try:
            if not self._validate_creds(service_user, service_password):
                raise ValueError("Invalid service account credentials")

        except Exception as e:
            print('ERROR: Unable to validate service account credentials.')
            raise e 

    def _validate_creds(self, username, password) -> bool:
        """
        This function validates usernames & passwords in namespaces for which the service account has READ permissions.
        Use this decorator to protect routes on namespaces you control. 

        If the service account does not have permission in the provided namespace, a 403 is returned regardless of
        the validity of the provided credentials. Ensure that the service account has read perms on the namespace
        that you are trying to protect.
        
        AAF determines the namespace from the username. Ex:
            sm663k@csp.att.com -> user sm663k in AAF namespace 'com.att.csp'
            example@your.namespace.att.com -> user example in AAF namespace 'com.att.namespace.your'

        More info: https://wiki.web.att.com/pages/viewpage.action?pageId=738754793

        WARN: This method cannot validate human user credentials (user@csp.att.com) unless a service account
        with READ permissions on com.att.csp is used.
        """
        route_uri = '/authn/validate'
        route_headers = {
            'Content-Type': 'application/json'
        }
        route_data = json.dumps({"id":username,"password":password})

        resp = requests.request(
            method='POST', 
            url='{root}{route}'.format(root=self.root_uri, route=route_uri), 
            headers=route_headers, 
            auth=(self.service_user, self.service_password),
            data=route_data
            )


        if resp.status_code == requests.codes.ok: # pylint: disable=no-member
            return True

        return False

    def has_perm(self, perm) -> bool:
        """
        Checks if the requesting user has the specified AAF permission
        """
        auth = flask.request.authorization
        route_uri = '/authz/perms/user/{user}'.format(user=auth.username)
        route_headers = {
            'Content-Type': 'application/json'
        }

        resp = requests.request(
            method='GET', 
            url='{root}{route}'.format(root=self.root_uri, route=route_uri),
            headers=route_headers, 
            auth=(self.service_user, self.service_password)
            )

        # pylint: disable=no-member
        if resp.status_code == requests.codes.ok: 
            return True

        return False

    def has_role(self, role) -> bool:
        """
        Checks if the requesting user has the specified AAF role
        """
        auth = flask.request.authorization
        route_uri = '/authz/users/{user}/{role}'.format(user=auth.username, role=role)
        route_headers = {
            'Accept': 'application/json'
        }

        resp = requests.request(
            method='GET', 
            url='{root}{route}'.format(root=self.root_uri, route=route_uri),
            headers=route_headers, 
            auth=(self.service_user, self.service_password)
            )

        if resp.status_code == requests.codes.ok: # pylint: disable=no-member
            # Dictionary will be empty if the user does not have that role - empty dicts are falsy
            if resp.json():
                return True

        return False

    def is_member_or_admin(self, namespace):
        """
        Checks if the requesting user is a member or admin of the specified namespace
        """
        auth = flask.request.authorization
        route_uri = '/authz/nss/either/{user}'.format(user=auth.username)
        route_headers = {
            'Accept': 'application/json'
        }

        resp = requests.request(
            method='GET', 
            url='{root}{route}'.format(root=self.root_uri, route=route_uri),
            headers=route_headers, 
            auth=(self.service_user, self.service_password)
            )

        if resp.status_code == requests.codes.ok: # pylint: disable=no-member
            # Returns a dict of the user's namespaces - check that the passed namespace
            # is in the dict
            print(resp.json())
            if namespace in resp.json():
                return True

        return False

    def ns_admin(self, user):
        """
        Returns the namespaces where the specified user is an admin.
        """
        raise NotImplementedError
        # GET /authz/nss/admin/<user>