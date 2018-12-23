import graphene as g
import nengo.params as p


class GqlFieldsFromParams(g.ObjectType):
    paramTypeToGqlType = {
        p.StringParam: g.String,
        p.BoolParam: g.Boolean,
        p.NumberParam: g.Float,
        p.IntParam: g.Int,
    }

    def __init__(self, obj):
        super().__init__()
        self._obj = obj

    def __init_subclass__(cls, backing_class, **kwargs):
        unsupported_params = []

        for param_name in p.iter_params(backing_class):
            param = getattr(backing_class, param_name)
            if (param.name not in vars(cls)
                    and type(param) in cls.paramTypeToGqlType):
                cls.bind_param(param)
            else:
                unsupported_params.append(param)

        setattr(cls, 'unsupported_params', tuple(unsupported_params))
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
