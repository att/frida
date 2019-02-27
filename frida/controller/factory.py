# Copyright (c) 2019 AT&T Intellectual Property. All rights reserved.

import frida.database as fdb
from frida.controller.base import BaseController
from frida.controller.mariadb import MariaDbController
from frida.controller.vertica import VerticaController
from frida.controller.postgres import PostgresController
from frida.controller.mongodb import MongoDbController


class ControllerFactory:
    """
    Takes a Frida Database and returns a Controller capable of profiling 
    that DB tech_type
    """
    
    @classmethod
    def get_controller(cls, database: fdb.Database) -> BaseController:

        return cls._init_controller_subclass(database.tech_type)

    @classmethod
    def _init_controller_subclass(cls, tech_type: str):
        """
        Instantiates the subclass of BaseController corresponding to the passed tech_type
        """
        if tech_type not in fdb.DB_TECH_TYPES:
            raise ValueError("Error: tech_type must be enumerated in database.DB_TECH_TYPES")
        
        elif tech_type == 'mariadb':
            return MariaDbController()

        elif tech_type == 'vertica':
            return VerticaController()

        elif tech_type == 'postgres':
            return PostgresController()

        elif tech_type == 'mongodb':
            return MongoDbController()

        else:
            raise ValueError("No Controller subclass matching the passed tech_type")
