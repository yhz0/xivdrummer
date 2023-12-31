# validate.py
# validate a config file against the json schema

import jsonschema
import json

# validate config.json against config.schema.json
with open('config.json') as f:
    config = json.load(f)

with open('config.schema.json') as f:
    schema = json.load(f)

jsonschema.validate(config, schema)
