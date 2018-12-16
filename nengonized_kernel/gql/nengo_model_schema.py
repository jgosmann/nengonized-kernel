from graphene import List, NonNull, ObjectType, String
import nengo

from .meta import GqlFieldsFromParams


class Ensemble(GqlFieldsFromParams, backing_class=nengo.Ensemble):
    pass


class Node(GqlFieldsFromParams, backing_class=nengo.Node):
    pass


class Network(ObjectType):
    label = String()
    ensembles = NonNull(List(NonNull(Ensemble)))
    nodes = NonNull(List(NonNull(Node)))

    def __init__(self, net):
        super()
        self._net = net

    def resolve_label(self, info):
        return self._net.label

    def resolve_ensembles(self, info):
        return [Ensemble(ens) for ens in self._net.ensembles]

    def resolve_nodes(self, info):
        return [Node(node) for node in self._net.nodes]
