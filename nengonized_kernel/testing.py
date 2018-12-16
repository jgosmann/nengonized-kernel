import nengo


dummy_model = '''
import nengo

with nengo.Network(label='dummy') as model:
    pass
'''


dummy_templates = {
    nengo.Ensemble: lambda **kwargs: nengo.Ensemble(10, 1, **kwargs),
    nengo.Node: lambda **kwargs: nengo.Node(0., **kwargs),
}


def create_dummy(type_, **kwargs):
    return dummy_templates[type_](**kwargs)
