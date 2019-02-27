# Copyright (c) 2019 AT&T Intellectual Property. All rights reserved.

DB_TECH_TYPES = [
    'mariadb',
    'vertica', 
    'postgres',
    'oracle',
    'mongodb'
]

class Database(object):
    def __init__(self, host, port, user, passwd, database, tech_type: "Database type from DB_TECH_TYPES"):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database

        #To perform @property validation
        self.tech_type = tech_type

    @property
    def tech_type(self):
        return self._tech_type

    @tech_type.setter
    def tech_type(self, tech_type):
        if tech_type not in DB_TECH_TYPES:
            raise ValueError("tech_type must be enumerated in frida.database.DB_TECH_TYPES.")
        self._tech_type = tech_type

    @tech_type.deleter
    def tech_type(self):
        del self._tech_type
