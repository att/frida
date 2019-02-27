# Copyright (c) 2019 AT&T Intellectual Property. All rights reserved.

import ast
import pymongo as pym
import frida.database as fdb
from frida.adapter.base import Manifest, BaseAdapter

class MongoDbAdapter(BaseAdapter):

    def __init__(self):
        # To gain self._bound_host & _bound_cnx
        super().__init__()
        self.tech_type = 'mongodb'

    @property
    def bound_cnx(self):
        """
        The open connection to the bound host.
        """
        return self._bound_cnx

    @bound_cnx.setter
    def bound_cnx(self, cnx):
        """
        The open connection to the bound host.
        """
        if self._bound_cnx:
            print('Closing existing connection...')
            self._bound_cnx.close()
        
        self._bound_cnx = cnx

    # Tech-specific deleter for the parent @property bound_cnx
    @bound_cnx.deleter
    def bound_cnx(self):
        """
        Close open connections before un-binding the connection; tech-specific
        """
        self._bound_cnx.close()
        del self._bound_cnx

    def bind_host(self, database: fdb.Database):
        """
        Bind this Adapter to a target Database; opens a connection to the passed DB and assigns
        the connection object to self._bound_cnx
        """
        try:
            self.bound_cnx = self._connect(database)
            self.bound_host = database

        except Exception as err:
            print("An error occured while binding to the database: {err}".format(err=err))
            return None

    def _connect(self, target_db: fdb.Database) -> pym.database:
        """
        Open a connection to the passed database, return a pymongo Database
        """
        try:
            cnx = pym.MongoClient(
                host = target_db.host,
                port = target_db.port,
                username = target_db.user,
                password = target_db.passwd,
                )

            # MongoClient constructor does not throw on conn failure
            # Check w/ cheap command
            # https://api.mongodb.com/python/current/api/pymongo/mongo_client.html#pymongo.mongo_client.MongoClient
            #__ = cnx.admin.command('ismaster')
            
            # Return the database object that allows commands, not the client
            # Must bind different adapters to each db on host
            return cnx[target_db.database]

        except Exception as err:
            print("An error occured while connecting to the database: {err}".format(err=err))
            return None

    def _format_row(self, row, return_format: dict):
        """
        Overloaded pass-through method - pymongo already returns JSON,
        so just return each row.
        
        """
        return row

    def _prepare_query(self, manifest: Manifest):
        """
        Overloaded method to support direct passing of frida.base.Manifests

        MongoDbAdapter._query expects prepared_q to be of type dict, use
        ast.literal_eval to convert strings to dicts safely
        """
        return ast.literal_eval(
            manifest.query_template.format(**manifest.query_bindings)
        )

    def _query(self, prepared_q: dict):
        """
        Execute a prepared query (DICTIONARY!) against the bound database & 
        return a cursor to the result set
        """
        return self.bound_cnx.command(prepared_q)
