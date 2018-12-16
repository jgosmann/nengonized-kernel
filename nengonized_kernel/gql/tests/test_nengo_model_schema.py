import nengo
import pytest

from nengonized_kernel.gql.schema import Context, schema
from nengonized_kernel.gql.testing import assert_gql_data_equals
from nengonized_kernel.testing import create_dummy


@pytest.mark.parametrize('nengo_type', [nengo.Ensemble, nengo.Node])
def test_can_query_objects_from_model(nengo_type):
    with nengo.Network() as model:
        create_dummy(nengo_type, label="label")

    query_name = nengo_type.__name__.lower() + 's'
    result = schema.execute(
        f'{{ model {{ {query_name} {{ label }} }} }}', context=Context(model))

    assert_gql_data_equals(result, {
        'model': {
            query_name: [{
                'label': "label"
            }]
        }
    })
