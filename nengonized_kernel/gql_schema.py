import warnings

import graphene as g
import nengo
import nengo.params as p
from nengo.params import iter_params


class GqlFieldsFromParams(g.ObjectType):
    paramTypeToGqlType = {
        p.StringParam: g.String,
        p.BoolParam: g.Boolean,
        p.NumberParam: g.Float,
        p.IntParam: g.Int,
    }

    def __init__(self, obj):
        self._obj = obj

    def __init_subclass__(cls, backing_class, **kwargs):
        for param_name in iter_params(backing_class):
            param = getattr(backing_class, param_name)
            if (param.name not in vars(cls)
                    and type(param) in cls.paramTypeToGqlType):
                cls.bind_param(param)
            else:
                warnings.warn(
                    f"Cannot bind param '{cls.__name__}.{param.name}' of type "
                    f"'{type(param).__name__}' because corresponding Graphene "
                    f"type is unknown.")
        super().__init_subclass__(**kwargs)

    @classmethod
    def bind_param(cls, param):
        field_type = cls.paramTypeToGqlType[type(param)]
        if not param.optional:
            field_type = g.NonNull(field_type)
        else:
            field_type = field_type()
        setattr(cls, param.name, field_type)
        setattr(cls, 'resolve_' + param.name,
                lambda self, info, name=param.name: getattr(self._obj, name))


class Ensemble(GqlFieldsFromParams, backing_class=nengo.Ensemble):
    pass


class Node(GqlFieldsFromParams, backing_class=nengo.Node):
    pass


class Network(g.ObjectType):
    ensembles = g.NonNull(g.List(g.NonNull(Ensemble)))
    nodes = g.NonNull(g.List(g.NonNull(Node)))

    def __init__(self, net):
        super()
        self._net = net

    def resolve_ensembles(self, info):
        return [Ensemble(ens) for ens in self._net.ensembles]

    def resolve_nodes(self, info):
        return [Node(node) for node in self._net.nodes]


class RootQuery(g.ObjectType):
    model = g.Field(Network)

    def resolve_model(self, info):
        return Network(info.context)


nengo_model_schema = g.Schema(query=RootQuery)
