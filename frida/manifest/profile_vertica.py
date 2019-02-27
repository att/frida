from frida.manifest.base import Manifest

# name of the metadata schema for Vertica
MD_CATALOG = 'v_catalog'

_vertica_get_models = Manifest(
            name='get_models',
            tech_type = 'vertica',
            query_template="SELECT SCHEMA_NAME FROM {catalog}.SCHEMATA;",
            query_bindings={'catalog': MD_CATALOG},
            return_format={
                'SCHEMA_NAME': 0
            })   

_vertica_get_entities = Manifest(
    name='get_entities',
    tech_type = 'vertica',
    query_template="SELECT TABLE_NAME, TABLE_SCHEMA, OWNER_NAME, \
                IS_SYSTEM_TABLE, IS_FLEXTABLE, CREATE_TIME FROM \
                {catalog}.TABLES WHERE TABLE_SCHEMA='{schema}';",
    query_bindings={'catalog': MD_CATALOG},
    return_format={
        'TABLE_NAME': 0,
        'TABLE_SCHEMA': 1,
        'OWNER_NAME': 2,
        'IS_SYSTEM_TABLE': 3,
        'IS_FLEXTABLE': 4,
        'TABLE_CREATE_TIME': 5
    })

_vertica_get_attributes = Manifest(
    name='get_attributes',
    tech_type = 'vertica',
    query_template="SELECT COLUMN_NAME, TABLE_NAME, \
    DATA_TYPE, DATA_TYPE_LENGTH, NUMERIC_PRECISION, \
    ORDINAL_POSITION, IS_NULLABLE, IS_IDENTITY FROM \
    {catalog}.COLUMNS WHERE TABLE_SCHEMA='{schema}' \
    AND TABLE_NAME='{entity}';",
    query_bindings={'catalog': MD_CATALOG},
    return_format={
        'COLUMN_NAME': 0,
        'TABLE_NAME': 1,
        'DATA_TYPE': 2,
        'TYPE_MAX_LEN': 3,
        'NUMERIC_PRECISION': 4,
        'ORDINAL_POSITION': 5,
        'IS_NULLABLE': 6,
        'IS_IDENTITY': 7
    })

_vertica_get_views = Manifest(
    name='get_views',
    tech_type = 'vertica',
    query_template="SELECT TABLE_NAME, TABLE_SCHEMA, OWNER_NAME, \
                CREATE_TIME FROM \
                {catalog}.VIEWS WHERE TABLE_SCHEMA='{schema}';",
    query_bindings={'catalog': MD_CATALOG},
    return_format={
        'VIEW_NAME': 0,
        'TABLE_SCHEMA': 1,
        'OWNER_NAME': 2,
        'VIEW_CREATE_TIME': 3
    })

_vertica_get_view_attributes = Manifest(
    name='get_attributes',
    tech_type = 'vertica',
    query_template="SELECT COLUMN_NAME, TABLE_NAME, \
    DATA_TYPE, DATA_TYPE_LENGTH, NUMERIC_PRECISION, \
    ORDINAL_POSITION FROM \
    {catalog}.VIEW_COLUMNS WHERE TABLE_SCHEMA='{schema}' \
    AND TABLE_NAME='{view}';",
    query_bindings={'catalog': MD_CATALOG},
    return_format={
        'COLUMN_NAME': 0,
        'VIEW_NAME': 1, #aliasing table_name to view_name
        'DATA_TYPE': 2,
        'DATA_TYPE_LENGTH': 3,
        'NUMERIC_PRECISION': 4,
        'ORDINAL_POSITION': 5
    })
