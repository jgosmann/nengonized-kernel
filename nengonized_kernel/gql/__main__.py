import json

from .schema import schema

print(json.dumps({'data': schema.introspect()}))
