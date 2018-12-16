import graphene
import nengo

from nengonized_kernel.gql.meta import GqlFieldsFromParams


class TestGqlFieldsFromParams(object):
    def test_binds_param(self):
        class ParamClass(object):
            param = nengo.params.IntParam('param', default=42, optional=True)

        class ObjType(GqlFieldsFromParams, backing_class=ParamClass):
            pass

        assert isinstance(ObjType.param, graphene.Int)
        assert ObjType(ParamClass()).resolve_param(None) == 42

    def test_binds_non_optional_param_as_non_null(self):
        class ParamClass(object):
            param = nengo.params.IntParam('param', default=42, optional=False)

        class ObjType(GqlFieldsFromParams, backing_class=ParamClass):
            pass

        assert isinstance(ObjType.param, graphene.NonNull)
        assert ObjType(ParamClass()).resolve_param(None) == 42

    def test_provides_list_of_unsupported_fields(self):
        class UnsupportedParam(nengo.params.Parameter):
            pass

        class ParamClass(object):
            unsupported_param = UnsupportedParam('unsupported_param')

        class ObjType(GqlFieldsFromParams, backing_class=ParamClass):
            pass

        assert ObjType.unsupported_params == (ParamClass.unsupported_param,)
