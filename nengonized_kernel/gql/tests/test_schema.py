from nengonized_kernel.gql.schema import Context, schema
from nengonized_kernel.gql.testing import assert_gql_data_equals
from nengonized_kernel.model_loader import ExecutionError, ModelLoader
from nengonized_kernel.testing import dummy_model, MatchAny, MatchRegex


query_errors = '''
    {
        errors {
            message,
            traceback { filename, lineno, name },
            filename,
            lineno,
            offset,
            text
        }
    }
'''


def create_syntax_error():
    code = 'import'
    try:
        ModelLoader().from_string(code)
    except ExecutionError as err:
        assert isinstance(err.inner_exception, SyntaxError)
        return err
    raise AssertionError(
            "Should have raised an ExecutionError wrapping a SyntaxError.")


def create_execution_error():
    code = 'x'
    try:
        ModelLoader().from_string(code)
    except ExecutionError as err:
        assert not isinstance(err.inner_exception, SyntaxError)
        return err
    raise AssertionError("Should have raised an ExecutionError.")


def create_general_non_execution_error():
    try:
        raise Exception("dummy exception")
    except Exception as err:
        return err


def test_can_query_syntax_errors():
    context = Context(errors=[create_syntax_error()])
    result = schema.execute(query_errors, context=context)
    assert_gql_data_equals(result, {
        'errors': [{
            'message': MatchRegex(".*invalid syntax"),
            'filename': '<string>',
            'lineno': 1,
            'offset': 7,
            'text': 'import\n',
            'traceback': None,
        }]
    })


def test_can_query_execution_errors():
    context = Context(errors=[create_execution_error()])
    result = schema.execute(query_errors, context=context)
    assert_gql_data_equals(result, {
        'errors': [{
            'message': MatchRegex(".*not defined"),
            'filename': '<string>',
            'lineno': 1,
            'offset': None,
            'text': None,
            'traceback': [{
                'filename': '<string>',
                'lineno': 1,
                'name': '<module>'
            }],
        }]
    })


def test_can_query_general_non_execution_errors():
    context = Context(errors=[create_general_non_execution_error()])
    result = schema.execute(query_errors, context=context)
    assert_gql_data_equals(result, {
        'errors': [{
            'message': "dummy exception",
            'filename': None,
            'lineno': None,
            'offset': None,
            'text': None,
            'traceback': [{
                'filename': MatchAny(str),
                'lineno': MatchAny(int),
                'name': 'create_general_non_execution_error'
            }],
        }]
    })

