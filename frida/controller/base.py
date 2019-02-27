# Copyright (c) 2019 AT&T Intellectual Property. All rights reserved.

"""
Controllers execute Manifests against Adapters to extract metadata from target hosts,
then format and return it as JSON
"""
import json
import frida.database as fdb
from frida.adapter.factory import AdapterFactory
from abc import ABC, abstractmethod

class BaseController(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def profile(self, target_db: fdb.Database):
        """
        Uses an Adapter to profile a database and returns its technical metadata to a JSON file

        NOTE: Some SQL types that appear in DB metadata (datetime) are not JSON
        serializable, so you must first ensure that json.dumps(obj, default=str) is properly set.
        
        See: json.dumps `default` param, frida.controller.mariadb for reference
        """

        adapter = AdapterFactory.get_bound_adapter(target_db)
        raise NotImplementedError("BaseController is abstract - you must instantiate a child class")
