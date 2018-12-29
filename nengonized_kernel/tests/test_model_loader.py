import os

import nengo
import pytest

from nengonized_kernel.model_loader import (
        ExecutionError, ModelLoader, ModelNotFoundError)
from nengonized_kernel.testing import dummy_model


class TestModelLoader(object):
    def test_loads_model_from_string(self):
        model, locals_dict = ModelLoader().from_string(dummy_model)
        assert isinstance(model, nengo.Network)
        assert model.label == 'dummy'
        assert locals_dict['model'] is model

    def test_does_not_change_working_directory(self):
        code = "import os; os.chdir('..')\n" + dummy_model
        expected = os.getcwd()
        ModelLoader().from_string(code)
        actual = os.getcwd()
        os.chdir(expected)  # prevent side-effects on other tests
        assert actual == expected

    def test_raises_ExecutionError_if_code_raises_exception(self):
        code = "import"
        with pytest.raises(ExecutionError) as excinfo:
            ModelLoader().from_string(code)
        assert isinstance(excinfo.value.__cause__, SyntaxError)

    def test_raises_ModelNotFoundError_if_model_is_not_defined(self):
        with pytest.raises(ModelNotFoundError):
            ModelLoader().from_string("")

    def test_sets_name(self):
        model, locals_dict = ModelLoader('name').from_string("""
import nengo
model = nengo.Network(label=__name__)
""")
        assert model.label == 'name'
