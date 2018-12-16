import nengo

from nengonized_kernel.model_loader import ModelLoader
from nengonized_kernel.testing import dummy_model


class TestModelLoader(object):
    def test_loads_model_from_string(self):
        model = ModelLoader().from_string(dummy_model)
        assert isinstance(model, nengo.Network)
        assert model.label == 'dummy'

    # TODO
    # workdir test!
    # error cases
    # __nengo_gui__ var/__file__
    # no model
