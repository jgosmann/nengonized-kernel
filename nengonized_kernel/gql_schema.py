from graphene import Field, List, NonNull, ObjectType, Schema, String


class NengoObject(ObjectType):
    label = String()

    def __init__(self, obj):
        super()
        self._obj = obj

    def resolve_label(self, info):
        return self._obj.label


class Ensemble(NengoObject):
    pass


class Node(NengoObject):
    pass


class Network(ObjectType):
    ensembles = NonNull(List(NonNull(Ensemble)))
    nodes = NonNull(List(NonNull(Node)))

    def __init__(self, net):
        super()
        self._net = net

    def resolve_ensembles(self, info):
        return [Ensemble(ens) for ens in self._net.ensembles]

    def resolve_nodes(self, info):
        return [Node(node) for node in self._net.nodes]


class RootQuery(ObjectType):
    model = Field(Network)

    def resolve_model(self, info):
        return Network(info.context)


nengo_model_schema = Schema(query=RootQuery)
