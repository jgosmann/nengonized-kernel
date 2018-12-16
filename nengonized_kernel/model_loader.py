from contextlib import contextmanager
import os


@contextmanager
def preserve_cwd():
    saved_cwd = os.getcwd()
    try:
        yield
    finally:
        os.chdir(saved_cwd)


class ModelLoader(object):
    def from_string(self, code):
        locals_dict = {}
        with preserve_cwd():
            exec(code, locals_dict)
        return locals_dict['model']
