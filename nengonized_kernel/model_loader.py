class ModelLoader(object):
    def from_string(self, code):
        locals_dict = {}
        exec(code, locals_dict)
        return locals_dict['model']
