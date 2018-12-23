from base64 import b64encode

import nengo
import pytest

from nengonized_kernel.gql.schema import Context, schema
from nengonized_kernel.gql.testing import assert_gql_data_equals
from nengonized_kernel.id_provider import IdProvider
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


@pytest.mark.parametrize('nengo_type', [nengo.Ensemble, nengo.Node])
def test_can_query_object_ids(nengo_type):
    with nengo.Network() as model:
        create_dummy(nengo_type, label="label")

    query_name = nengo_type.__name__.lower() + 's'
    result = schema.execute(
        f'{{ model {{ id, {query_name} {{ id }} }} }}', context=Context(
            model,
            id_provider=IdProvider(model, {'model': model}, prefix='no')))

    assert_gql_data_equals(result, {
        'model': {
            'id': b64encode('NengoNetwork:no:Network:model'.encode()).decode(),
            query_name: [{
                'id': b64encode(
                    (f'Nengo{nengo_type.__name__}:no:{nengo_type.__name__}:'
                    f'model.{query_name}[0]').encode()).decode()
            }]
        }
    })


def test_can_fetch_by_object_id():
    with nengo.Network() as model:
        ens = nengo.Ensemble(10, 1, label="Ensemble")

    id_provider = IdProvider(model, {'model': model, 'ens': ens}, prefix='no')
    key = b64encode(b'NengoEnsemble:no:Ensemble:ens').decode()

    result = schema.execute(
            f'{{ node(id: "{key}") {{ ... on NengoEnsemble {{ label }} }} }}',
            context=Context(model, id_provider=id_provider))

    assert_gql_data_equals(result, { 'node': { 'label': "Ensemble" } })
