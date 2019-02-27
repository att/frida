# Copyright (c) 2019 AT&T Intellectual Property. All rights reserved.

import json
import frida.database as fdb
import frida.manifest.profile_mongodb as modb
from frida.controller.base import BaseController
from frida.adapter.factory import AdapterFactory

class MongoDbController(BaseController):
    def __init__(self):
        pass

    def profile(self, target_db: fdb.Database):
        """
        Profiles a database and returns its technical metadata to a JSON file
        """
        adapter = AdapterFactory.get_bound_adapter(database=target_db)
        metadata = {"FRIDA.DATABASE": []}

        for model in adapter.execute(modb._mongo_get_db_stats):
            metadata["FRIDA.DATABASE"].append(model)

        
        return json.dumps(metadata)
