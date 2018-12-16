from nengonized_kernel.gql.schema import Context, schema
from nengonized_kernel.gql.testing import assert_gql_data_equals
from nengonized_kernel.testing import dummy_model


def test_mutate_model():
    context = Context()
    result = schema.execute(
        '''
            mutation test_replace_model($code: String) {
                replaceModel(code: $code) {
                    model { label }
                }
            }
        ''',
        variables={'code': dummy_model},
        context=context)

    assert_gql_data_equals(result, {
        'replaceModel': {
            'model': {
                'label': 'dummy'
            }
        }
    })
    assert context.model.label == 'dummy'

# TODO error cases
