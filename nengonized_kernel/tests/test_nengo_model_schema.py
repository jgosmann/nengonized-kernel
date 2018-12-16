from graphene.test import Client
import nengo
import pytest

from nengonized_kernel.gql_schema import GqlFieldsFromParams, nengo_model_schema


def assert_gql_data_equals(result, expected):
    assert not result.errors, str("\n".join(str(e) for e in result.errors))
    assert result.data == expected


def create_nengo_obj_dummy(nengo_type, **kwargs):
    typemap = {
        nengo.Ensemble: lambda **kwargs: nengo.Ensemble(10, 1, **kwargs),
        nengo.Node: lambda **kwargs: nengo.Node(0., **kwargs),
    }
    return typemap[nengo_type](**kwargs)


@pytest.mark.parametrize('nengo_type', [nengo.Ensemble, nengo.Node])
def test_can_query_objects_from_model(nengo_type):
    with nengo.Network() as model:
        create_nengo_obj_dummy(nengo_type, label="label")

    query_name = nengo_type.__name__.lower() + 's'
    result = nengo_model_schema.execute(
        f'{{ model {{ {query_name} {{ label }} }} }}', context=model)

    assert_gql_data_equals(result, {
        'model': {
            query_name: [{
                'label': "label"
            }]
        }
    })


def test_GqlFieldsFromParams_provides_list_of_unsupported_fields():
    class UnsupportedParam(nengo.params.Parameter):
        pass

    class ParamClass(object):
        unsupported_param = UnsupportedParam('unsupported_param')

    class ObjType(GqlFieldsFromParams, backing_class=ParamClass):
        pass

    assert ObjType.unsupported_params == (ParamClass.unsupported_param,)
