# Copyright (c) 2019 AT&T Intellectual Property. All rights reserved.

import json
import frida.database as fdb
import frida.manifest.profile_vertica as pvdb
from frida.controller.base import BaseController
from frida.adapter.factory import AdapterFactory

class VerticaController(BaseController):
    def __init__(self):
        pass

    def profile(self, target_db: fdb.Database):
        """
        Profiles a database and returns its technical metadata to a JSON file
        """
        adapter = AdapterFactory.get_bound_adapter(database=target_db)
        metadata = {"FRIDA.SCHEMAS": []}

        for model in adapter.execute(pvdb._vertica_get_models):
            schema_name = model['SCHEMA_NAME']

            tables = []
            pvdb._vertica_get_entities.add_bindings(catalog='v_catalog', schema=schema_name)
            for entity in adapter.execute(pvdb._vertica_get_entities):
                table_name = entity['TABLE_NAME']

                t_columns = []
                pvdb._vertica_get_attributes.add_bindings(catalog='v_catalog', schema=schema_name, entity=table_name)
                for t_attr in adapter.execute(pvdb._vertica_get_attributes):
                    t_columns.append(t_attr)

                entity["FRIDA.COLUMNS"] = t_columns
                tables.append(entity)

            views = []
            pvdb._vertica_get_views.add_bindings(catalog='v_catalog', schema=schema_name)
            for view in adapter.execute(pvdb._vertica_get_views):
                view_name = view['VIEW_NAME']

                v_columns = []
                pvdb._vertica_get_view_attributes.add_bindings(catalog='v_catalog', schema=schema_name, view=view_name)
                for v_attr in adapter.execute(pvdb._vertica_get_view_attributes):
                    v_columns.append(v_attr)

                view["FRIDA.COLUMNS"] = v_columns
                views.append(view)

            model["FRIDA.TABLES"] = tables
            model["FRIDA.VIEWS"] = views
            metadata["FRIDA.SCHEMAS"].append(model)

        return json.dumps(metadata, default=str)
