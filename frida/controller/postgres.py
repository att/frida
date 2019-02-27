# Copyright (c) 2019 AT&T Intellectual Property. All rights reserved.

import json
import frida.database as fdb
import frida.manifest.profile_postgres as ppdb
from frida.controller.base import BaseController
from frida.adapter.factory import AdapterFactory

class PostgresController(BaseController):
    def __init__(self):
        pass

    def profile(self, target_db: fdb.Database):
        """
        Profiles a database and returns its technical metadata to a JSON file
        """
        adapter = AdapterFactory.get_bound_adapter(database=target_db)
        metadata = {"FRIDA.SCHEMAS": []}

        for model in adapter.execute(ppdb._postgres_get_models):
            schema_name = model['SCHEMA_NAME']

            tables = []
            ppdb._postgres_get_entities.add_bindings(schema=schema_name)
            for entity in adapter.execute(ppdb._postgres_get_entities):
                entity_name = entity['TABLE_NAME']

                t_columns = []
                ppdb._postgres_get_attributes.add_bindings(schema=schema_name, entity=entity_name)
                for t_attr in adapter.execute(ppdb._postgres_get_attributes):
                    t_columns.append(t_attr)

                entity["FRIDA.COLUMNS"] = t_columns
                tables.append(entity)

            views = []
            ppdb._postgres_get_views.add_bindings(schema=schema_name)
            for view in adapter.execute(ppdb._postgres_get_views):
                view_name = view['VIEW_NAME']

                v_columns = []
                ppdb._postgres_get_attributes.add_bindings(schema=schema_name, entity=view_name)
                for v_attr in adapter.execute(ppdb._postgres_get_attributes):
                    v_columns.append(v_attr)

                view["FRIDA.COLUMNS"] = v_columns
                views.append(view)

            model["FRIDA.TABLES"] = tables
            model["FRIDA.VIEWS"] = views
            metadata["FRIDA.SCHEMAS"].append(model)

        return json.dumps(metadata, default=str)