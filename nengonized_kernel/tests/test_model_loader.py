import os

import nengo
import pytest

from nengonized_kernel.model_loader import (
        ExecutionException, ModelLoader, NoModelException)
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

    def test_raises_ExecutionException_if_code_raises_exception(self):
        code = "import"
        with pytest.raises(ExecutionException) as excinfo:
            ModelLoader().from_string(code)
        assert isinstance(excinfo.value.__cause__, SyntaxError)

    def test_raises_ModelNotFoundException_if_model_is_not_defined(self):
        with pytest.raises(NoModelException):
            ModelLoader().from_string("")

    # TODO
    # __nengo_gui__ var/__file__
