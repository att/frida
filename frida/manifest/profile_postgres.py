from frida.manifest.base import Manifest

# Name of the metadata catalog for Postgres
MD_CATALOG = 'information_schema'

_postgres_get_models = Manifest(
            name='get_models',
            tech_type = 'postgres',
            query_template="SELECT SCHEMA_NAME FROM {catalog}.SCHEMATA;",
            query_bindings={'catalog': MD_CATALOG},
            return_format={
                'SCHEMA_NAME': 0
            })   

_postgres_get_entities = Manifest(
    name='get_entities',
    tech_type = 'postgres',
    query_template="SELECT TABLE_NAME FROM \
                {catalog}.TABLES WHERE TABLE_SCHEMA='{schema}' \
                AND TABLE_TYPE='BASE TABLE';",
    query_bindings={'catalog': MD_CATALOG},
    return_format={
        'TABLE_NAME': 0
    })

_postgres_get_views = Manifest(
    name='get_views',
    tech_type = 'postgres',
    query_template="SELECT TABLE_NAME, TABLE_SCHEMA, IS_UPDATABLE \
                FROM {catalog}.VIEWS WHERE TABLE_SCHEMA='{schema}';",
    query_bindings={'catalog': MD_CATALOG},
    return_format={
        'VIEW_NAME': 0,
        'TABLE_SCHEMA': 1,
        'IS_UPDATABLE': 2,
    })

_postgres_get_attributes = Manifest(
    name='get_attributes',
    tech_type = 'postgres',
    query_template="SELECT COLUMN_NAME, DATA_TYPE, \
    COLUMN_DEFAULT, IS_IDENTITY FROM \
    {catalog}.COLUMNS WHERE TABLE_SCHEMA='{schema}' \
    AND TABLE_NAME='{entity}';",
    query_bindings={'catalog': MD_CATALOG},
    return_format={
        'COLUMN_NAME': 0,
        'COLUMN_TYPE': 1,
        'COLUMN_DEFAULT': 2,
        'IS_IDENTITY': 3
    })
