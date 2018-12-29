import nengo
import re


dummy_model = '''
import nengo

with nengo.Network(label='dummy') as model:
    pass
'''


dummy_templates = {
    nengo.Ensemble: lambda **kwargs: nengo.Ensemble(10, 1, **kwargs),
    nengo.Node: lambda **kwargs: nengo.Node(0., **kwargs),
    nengo.Network: lambda **kwargs: nengo.Network(**kwargs),
}


def create_dummy(type_, **kwargs):
    return dummy_templates[type_](**kwargs)


class MatchRegex(object):
    def __init__(self, regex):
        self.regex = re.compile(regex)

    def __eq__(self, other):
        return self.regex.match(other)


class MatchAny(object):
    def __init__(self, type_):
        self.type = type_

    def __eq__(self, other):
        if isinstance(other, self.type):
            return True
        else:
            return False
