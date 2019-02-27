Copyright (c) 2019 AT&T Intellectual Property. All rights reserved.

# Introduction

Meet Frida - the FRIendly Database Analyzer

Developed for AT&T by Stuart Minshull, 2018

Technical Advisor is Don Subert (ds390s@att.com) of AT&T

# Configuration

Requires a config.py file, in the project root directory with the following properties:

 * AAF_SERVICE_AUTH = ('< full@qualified.aaf.id >', '< password >')
 * AAF_SERVICE_REALM = '<fully.qualified.aaf.perm.name>'
 * AAF_ROOT_URI = 'https://aaf.it.att.com:8095/proxy'  # or whatever alternate AAF root URI

# Client Requests

Example API request to analyze a MariaDB instance:

    curl -X POST \
      http://<service_host>:<service_port>/profile/ \
      -H 'Authorization: Basic <base64_encoded_credentials>' \
      -H 'Content-Type: application/json' \
      -d '{
        "host": "<db_host>",
        "port": <db_port>,
        "user": "<db_user>",
        "passwd": "<db_password",
        "database": "information_schema",
        "tech_type": "mariadb"
    }'
    
# AAF (Application Authorization Framework)

Access is controlled by the AAF project

https://github.com/att/AAF