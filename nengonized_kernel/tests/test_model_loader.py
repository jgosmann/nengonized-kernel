import os

import nengo

from nengonized_kernel.model_loader import ModelLoader
from nengonized_kernel.testing import dummy_model


class TestModelLoader(object):
    def test_loads_model_from_string(self):
        model = ModelLoader().from_string(dummy_model)
        assert isinstance(model, nengo.Network)
        assert model.label == 'dummy'

    def test_does_not_change_working_directory(self):
        code = "import os; os.chdir('..')\n" + dummy_model
        expected = os.getcwd()
        ModelLoader().from_string(code)
        actual = os.getcwd()
        os.chdir(expected)  # prevent side-effects on other tests
        assert actual == expected

    # TODO
    # error cases
    # __nengo_gui__ var/__file__
    # no model
