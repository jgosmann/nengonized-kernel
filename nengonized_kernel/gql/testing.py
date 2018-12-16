def assert_gql_data_equals(result, expected):
    assert not result.errors, str("\n".join(str(e) for e in result.errors))
    assert result.data == expected
