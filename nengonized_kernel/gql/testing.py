from collections import OrderedDict
from collections.abc import Iterable, Mapping


def _to_unordered_dict_deep(data):
    data = dict(data)
    for k, v in data.items():
        if isinstance(v, OrderedDict):
            data[k] = _to_unordered_dict_deep(v)
        elif isinstance(v, Iterable) and not isinstance(v, str):
            data[k] = [
                    _to_unordered_dict_deep(x) if isinstance(x, Mapping) else x
                    for x in v]
    return data


def assert_gql_data_equals(result, expected):
    assert not result.errors, str("\n".join(str(e) for e in result.errors))
    data = result.data
    if not isinstance(expected, OrderedDict):
        data = _to_unordered_dict_deep(data)
    assert data == expected
