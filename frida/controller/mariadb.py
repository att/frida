# Copyright (c) 2019 AT&T Intellectual Property. All rights reserved.

import json
import frida.database as fdb
import frida.manifest.profile_mariadb as pmdb
from frida.controller.base import BaseController
from frida.adapter.factory import AdapterFactory

class MariaDbController(BaseController):
    def __init__(self):
        pass

    def profile(self, target_db: fdb.Database):
        """
        Profiles a database and returns its technical metadata to a JSON file
        """
        adapter = AdapterFactory.get_bound_adapter(database=target_db)
        metadata = {"FRIDA.SCHEMAS": []}

        pmdb._maria_get_models.add_bindings(db=target_db.database)
        for model in adapter.execute(pmdb._maria_get_models):
            schema_name = model['SCHEMA_NAME']

            tables = []
            pmdb._maria_get_entities.add_bindings(db=target_db.database, schema=schema_name)
            for entity in adapter.execute(pmdb._maria_get_entities):
                table_name = entity['TABLE_NAME']

                columns = []
                pmdb._maria_get_attributes.add_bindings(db=target_db.database, schema=schema_name, entity=table_name)
                for attr in adapter.execute(pmdb._maria_get_attributes):
                    columns.append(attr)

                entity["FRIDA.COLUMNS"] = columns
                tables.append(entity)

            model["FRIDA.TABLES"] = tables
            metadata["FRIDA.SCHEMAS"].append(model)

        return json.dumps(metadata, default=str)