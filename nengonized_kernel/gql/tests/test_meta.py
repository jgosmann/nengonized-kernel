import graphene
import nengo

from nengonized_kernel.gql.meta import GqlFieldsFromParams


class GqlFieldsFromParamsTest(object):
    def test_binds_param():
        class ParamClass(object):
            param = IntParam(default=42)

        class ObjType(GqlFieldsFromParams, backing_class=ParamClass):
            pass

        assert isinstance(ObjType.param, graphene.Int)
        assert ObjType(ParamClass()).resolve_param == 42

    def test_provides_list_of_unsupported_fields():
        class UnsupportedParam(nengo.params.Parameter):
            pass

        class ParamClass(object):
            unsupported_param = UnsupportedParam('unsupported_param')

        class ObjType(GqlFieldsFromParams, backing_class=ParamClass):
            pass

        assert ObjType.unsupported_params == (ParamClass.unsupported_param,)
