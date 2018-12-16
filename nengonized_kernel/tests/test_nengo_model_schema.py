from graphene.test import Client
import nengo

from nengonized_kernel.gql_schema import nengo_model_schema


def test_can_query_ensembles():
    with nengo.Network() as model:
        ens = nengo.Ensemble(10, 1, label="ens")

    result = nengo_model_schema.execute(
        '{ model { ensembles { label } } }', context=model)

    assert result.data == {
        'model': {
            'ensembles': [{
                'label': "ens"
            }]
        }
    }
