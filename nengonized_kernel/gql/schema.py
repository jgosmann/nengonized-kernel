from graphene import Field, ObjectType, Schema

from .nengo_model_schema import Network


class Context(object):
    def __init__(self, model=None):
        self.model = model


class RootQuery(ObjectType):
    model = Field(Network)

    def resolve_model(self, info):
        return Network(info.context.model)


schema = Schema(query=RootQuery)
