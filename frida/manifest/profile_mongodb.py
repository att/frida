from frida.manifest.base import Manifest

# MongoDB is NOSQL & Schemaless - see frida.adapter.mongodb for notes
# on why MongoDB query templates look somewhat odd. Pymongo expects
# db.command() to have dictionary inputs - overloaded MongoDbAdapter 
# uses ast.literal_eval() to convert string query templates into dicts

# As such, you must use DOUBLE BRACES on the edge of the strings so that
# the braces remain after a str.format() operation.

# NOTE THAT IT IS VERY IMPORTANT TO HAVE A SPACE BETWEEN THE OUTER CURLY BRACES
# AND ANY OTHER CHARACTER
# Manifest binding will break if this is not honored!!

# MongoDbAdapter ignores return formats because Pymongo already returns J/BSON
_mongo_get_db_stats = Manifest(
    name='get_db_stats',
    tech_type='mongodb',
    query_template='{{ "dbStats": 1.0 }}',
    query_bindings={},
    return_format={}
)

_mongo_get_coll_names = Manifest(
    name='get_coll_names',
    tech_type='mongodb',
    query_template='{{ "listCollections": 1.0, "authorizedCollections": True, "nameOnly": True }}',
    query_bindings={},
    return_format={}
    )

_mongo_get_coll_stats = Manifest(
    name='get_coll_stats',
    tech_type='mongodb',
    query_template='{{ "collStats": "{collection}" }}',
    query_bindings={},
    return_format={}
    )  