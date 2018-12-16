from contextlib import contextmanager
import os


@contextmanager
def preserve_cwd():
    saved_cwd = os.getcwd()
    try:
        yield
    finally:
        os.chdir(saved_cwd)


class ExecutionException(Exception):
    pass


class NoModelException(Exception):
    pass


class ModelLoader(object):
    # TODO redirect stdout/stderr/stdin
    def from_string(self, code):
        locals_dict = {}
        try:
            with preserve_cwd():
                exec(code, locals_dict)
        except Exception as err:
            raise ExecutionException from err
        try:
            return locals_dict['model']
        except KeyError:
            raise NoModelException("No 'model' declared.")
