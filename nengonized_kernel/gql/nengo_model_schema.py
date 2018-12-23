from graphene import AbstractType, List, NonNull, ObjectType, relay, String
import nengo

from .meta import GqlFieldsFromParams


class IdProviderNode(object):
    @classmethod
    def get_node(cls, info, id_key):
        return cls(info.context.id_provider.reverse_lookup(id_key))


class NengoObject(IdProviderNode):
    def resolve_id(self, info):
        return info.context.id_provider[self._obj]


class NengoEnsemble(
        GqlFieldsFromParams,
        NengoObject,
        backing_class=nengo.Ensemble,
        interfaces=[relay.Node]):
    pass


class NengoNode(
        GqlFieldsFromParams,
        NengoObject,
        backing_class=nengo.Node,
        interfaces=[relay.Node]):
    pass


class NengoNetwork(ObjectType, IdProviderNode, interfaces=[relay.Node]):
    label = String()
    ensembles = NonNull(List(NonNull(NengoEnsemble)))
    nodes = NonNull(List(NonNull(NengoNode)))

    def __init__(self, net):
        super().__init__()
        self._net = net

    @classmethod
    def get_node(cls, info, id_key):
        return NengoNetwork(info.context.id_provider.reverse_lookup(id_key))

    def resolve_id(self, info):
        return info.context.id_provider[self._net]

    def resolve_label(self, info):
        return self._net.label

    def resolve_ensembles(self, info):
        return [NengoEnsemble(ens) for ens in self._net.ensembles]

    def resolve_nodes(self, info):
        return [NengoNode(node) for node in self._net.nodes]
