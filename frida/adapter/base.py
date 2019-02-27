# Copyright (c) 2019 AT&T Intellectual Property. All rights reserved.

import re
import frida.database as fdb
from frida.manifest.base import Manifest
from abc import ABC, abstractmethod

class BaseAdapter(ABC):
    """
    Abstract parent class for tech-specific database adapters
    """

    def __init__(self):
        self._bound_host = None
        self._bound_cnx = None
        self.tech_type = None

    def __enter__(self):
        '''
        Required to use this class as a context manager
        '''
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        '''
        Leaving context - close the bound_host's open cursors & connections
        '''
        del self.bound_host
        
    @property
    def bound_host(self) -> fdb.Database:
        """
        The database host that this Adapter been bound to.
        """
        return self._bound_host

    @bound_host.setter
    def bound_host(self, host: fdb.Database):
        """
        The database host that this Adapter been bound to.
        """
        if not isinstance(host, fdb.Database):
            raise TypeError("Error: host must be of type frida.Database")
        self._bound_host = host

    @bound_host.deleter
    def bound_host(self):
        """
        The database host that this Adapter been bound to.
        """
        del self.bound_cnx
        del self._bound_host

    @property
    @abstractmethod
    def bound_cnx(self):
        """
        The open connection to the bound host.
        """
        raise NotImplementedError("BaseAdapter is abstract; you must instantiate a subclass.")

    @abstractmethod
    def bind_host(self, database: fdb.Database):
        """
        Binds this Adapter to a target Database; opens a connecton to the DB and assigns
        self.bound_host to an object that can execute queries.
        (cursor, connection, etc. depending on tech)
        """
        raise NotImplementedError("BaseAdapter is abstract; you must instantiate a subclass.")

    @abstractmethod
    def _connect(self):
        """
        Used by Adapter.bind_host() to open a connection to the host during binding.
        Tech specific
        """
        raise NotImplementedError("BaseAdapter is abstract; you must instantiate a subclass.")

    @abstractmethod
    def _query(self, prepared_q):
        """
        Execute a prepared statement against the bound database & return an iterable
        """
        raise NotImplementedError("BaseAdapter is abstract; you must instantiate a subclass.")

    def _prepare_query(self, manifest: Manifest):
        """
        Overloaded method to support direct passing of frida.base.Manifests
        """
        return manifest.query_template.format(**manifest.query_bindings)

    def _format_row(self, row, return_format: dict):
        """
        Formats a row returned by a query according to the 
        name-index map provided in return_format
        """
        formatted_row = {}
        for key, idx in return_format.items():
            formatted_row[key] = row[idx]

        return formatted_row
    
    def _format_row(self, row, manifest: Manifest):
        """
        Formats a row returned by a query according to the 
        return_format specified in the passed Manifest
        """
        formatted_row = {}
        for key, idx in manifest.return_format.items():
            formatted_row[key] = row[idx]

        return formatted_row

    def execute(self, manifest: Manifest):
        """
        Uses a passed Manifest to query the bound host and return
        the result set as a dict according to Manifest's return format
        """
        if not manifest.seal():
            raise RuntimeError("Manifests must be sealed before querying! \
                                See: Manifest.seal()")

        if manifest.tech_type != self.tech_type:
            raise TypeError("Adapters can only execute Manifests that share their tech_type: \
                            Adapter: {selftype} vs Manifest: {manifest_type}! \
                            See: database.DB_TECH_TYPES".format(
                                selftype=self.tech_type, manifest_type=manifest.tech_type)
                            )

        # Generator for easy iteration, depends on the cursor staying alive
        def yield_formatted(result_cursor):
            for row in result_cursor:
                formatted = self._format_row(row, manifest)
                yield formatted

            # raise StopIteration

        # pytest: disable
        return yield_formatted(self._query(self._prepare_query(manifest)))
