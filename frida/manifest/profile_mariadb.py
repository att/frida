from frida.manifest.base import Manifest

# MariaDB information schema is accessible from any db

_maria_get_models = Manifest(
    name='get_models',
    tech_type = 'mariadb',
    query_template="SELECT SCHEMA_NAME FROM {db}.SCHEMATA;",
    query_bindings={},
    return_format={
        'SCHEMA_NAME': 0
    })   

_maria_get_entities = Manifest(
    name='get_entities',
    tech_type = 'mariadb',
    query_template="SELECT TABLE_NAME, TABLE_COMMENT, \
                TABLE_ROWS, CREATE_TIME, UPDATE_TIME FROM \
                {db}.TABLES WHERE TABLE_SCHEMA='{schema}' \
                AND TABLE_TYPE='BASE TABLE';",
    query_bindings={},
    return_format={
        'TABLE_NAME': 0,
        'TABLE_DESC': 1,
        'TABLE_ROWS': 2,
        'TABLE_CREATE_TIME': 3,
        'TABLE_UPDATE_TIME': 4
    })

_maria_get_attributes = Manifest(
    name='get_attributes',
    tech_type = 'mariadb',
    query_template="SELECT COLUMN_NAME, COLUMN_TYPE, \
    IS_NULLABLE, COLUMN_KEY FROM \
    {db}.COLUMNS WHERE TABLE_SCHEMA='{schema}' \
    AND TABLE_NAME='{entity}';",
    query_bindings={},
    return_format={
        'COLUMN_NAME': 0,
        'COLUMN_TYPE': 1,
        'IS_NULLABLE': 2,
        'COLUMN_KEY_TYPE': 3
    })
