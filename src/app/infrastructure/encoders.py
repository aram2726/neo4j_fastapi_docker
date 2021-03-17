import json

from neo4j.graph import Node

from src.app.core.entities import BaseEntity


class ResponseEncoder(json.JSONEncoder):
    def default(self, instance):
        if issubclass(instance.__class__, Node):
            data = {k: instance[k] for k in instance.keys()}
            return data
        if issubclass(instance.__class__, BaseEntity):
            data = instance.serialize()
            return {**data}
        else:
            return str(instance)
        return super().default(instance)
