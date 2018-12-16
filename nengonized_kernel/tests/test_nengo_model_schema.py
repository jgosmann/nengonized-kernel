from graphene.test import Client
import nengo

from nengonized_kernel.gql_schema import nengo_model_schema


def assert_gql_data_equals(result, expected):
    assert not result.errors, str("\n".join(str(e) for e in result.errors))
    assert result.data == expected


def test_can_query_ensembles_from_model():
    with nengo.Network() as model:
        ens = nengo.Ensemble(10, 1, label="ens")

    result = nengo_model_schema.execute(
        '{ model { ensembles { label } } }', context=model)


    assert_gql_data_equals(result, {
        'model': {
            'ensembles': [{
                'label': "ens"
            }]
        }
    })


def test_can_query_nodes_from_model():
    with nengo.Network() as model:
        node = nengo.Node(lambda t: t, label="node")

    result = nengo_model_schema.execute(
        '{ model { nodes { label } } }', context=model)


    assert_gql_data_equals(result, {
        'model': {
            'nodes': [{
                'label': "node"
            }]
        }
    })
