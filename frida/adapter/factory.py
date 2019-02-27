# Copyright (c) 2019 AT&T Intellectual Property. All rights reserved.

import frida.database as fdb
from frida.adapter.base import BaseAdapter
from frida.adapter.mariadb import MariaDbAdapter
from frida.adapter.vertica import VerticaAdapter
from frida.adapter.postgres import PostgresAdapter
from frida.adapter.mongodb import MongoDbAdapter


class AdapterFactory:
    """
    Receives Database objects and returns properly initialized Adapter that
    are bound to the passed Database
    """
    @classmethod
    def get_unbound_adapter(cls, tech_type) -> BaseAdapter: 
        """
        Returns an unbound Adapter subclass matching the specified tech_type
        """
        return cls._init_adapter_subclass(tech_type)
    
    @classmethod
    def get_bound_adapter(cls, database: fdb.Database) -> BaseAdapter:

        adapter = cls._init_adapter_subclass(database.tech_type)
        adapter.bind_host(database)

        return adapter

    @classmethod
    def _init_adapter_subclass(cls, tech_type: str) -> BaseAdapter:
        """
        Instantiates the subclass of Adapter corresponding to the passed tech_type
        """
        tech_type = tech_type.lower()

        if tech_type not in fdb.DB_TECH_TYPES:
            raise ValueError("Error: tech_type must be enumerated in database.DB_TECH_TYPES")
        
        elif tech_type == 'mariadb':
            return MariaDbAdapter()

        elif tech_type == 'vertica':
            return VerticaAdapter()

        elif tech_type == 'postgres':
            return PostgresAdapter()

        elif tech_type == 'mongodb':
            return MongoDbAdapter()

        else:
            raise ValueError("No Adapter subclass matching the passed tech_type")

    @classmethod
    def check_valid_type(cls, type_str) -> bool:
        """
        Returns a Boolean indicating if the passed str is a valid DB_TECH_TYPE
        """
        return type_str in fdb.DB_TECH_TYPES

    @classmethod
    def get_valid_types(cls) -> list:
        """
        Returns the list of valid DB_TECH_TYPEs
        """
        return fdb.DB_TECH_TYPES
