# Copyright (c) 2019 AT&T Intellectual Property. All rights reserved.

import vertica_python
import frida.database as fdb
from frida.adapter.base import Manifest, BaseAdapter

class VerticaAdapter(BaseAdapter):

    def __init__(self):
        # To gain self._bound_host & _bound_cnx
        super().__init__()
        self.tech_type = 'vertica'

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

    def _connect(self, target_db: fdb.Database):
        """
        Open a connection to the passed database
        """
        try:
            cnx = vertica_python.connect(
                host = target_db.host,
                port = target_db.port,
                user = target_db.user,
                password = target_db.passwd,
                database = target_db.database
                )
            
            return cnx

        except Exception as err:
            print("An error occured while connecting to the database: {err}".format(err=err))
            return None

    def _query(self, prepared_q):
        """
        Execute a prepared query against the bound database & 
        return a cursor to the result set
        """
        # Vertica SDK only supports 1 cursor per connection
        # https://github.com/uber/vertica-python/blob/master/vertica_python/vertica/connection.py#L61

        cursor = self._connect(self.bound_host).cursor()
        cursor.execute(prepared_q)

        # SDK cursors do not impl __iter__ - hide the call to .iterate() in a closure
        def yield_row(prep_cursor):
            for row in prep_cursor.iterate():
                yield row

            raise StopIteration
        
        return yield_row(cursor)
