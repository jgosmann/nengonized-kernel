from graphene import Field, Mutation, ObjectType, Schema, String

from .nengo_model_schema import Network
from ..model_loader import ModelLoader


class Context(object):
    def __init__(self, model=None):
        self.model = model


class RootQuery(ObjectType):
    model = Field(Network)

    def resolve_model(self, info):
        return Network(info.context.model)


class ReplaceModel(Mutation):
    class Arguments:
        code = String()

    model = Field(Network)

    def mutate(self, info, code):
        info.context.model = ModelLoader().from_string(code)
        return ReplaceModel(model=Network(info.context.model))


class Mutations(ObjectType):
    replaceModel = ReplaceModel.Field()


schema = Schema(query=RootQuery, mutation=Mutations)
