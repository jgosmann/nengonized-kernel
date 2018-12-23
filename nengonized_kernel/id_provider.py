import weakref

import nengo


class IdProvider(object):
    valid_types = {
        nengo.Network: 'Network',
        nengo.Ensemble: 'Ensemble',
        nengo.Node: 'Node',
    }

    def __init__(self, model, locals_dict=None, prefix='no'):
        self.prefix = prefix
        self._unique_name_map = weakref.WeakKeyDictionary()
        self._type_map = weakref.WeakKeyDictionary()
        self._reverse_map = weakref.WeakValueDictionary()
        if locals_dict:
            self._scan_locals(locals_dict)
        self._scan_networks(model)
        self._scan_standard_lists(model)

    def _scan_locals(self, locals_dict):
        for k, v in locals_dict.items():
            self._process_candidate(v, k)

    def _scan_networks(self, net):
        to_process = [net]
        while len(to_process) > 0:
            net = to_process.pop()
            for attr_name in dir(net):
                value = getattr(net, attr_name)
                self._process_candidate(
                        value, f'{self._unique_name_map[net]}.{attr_name}')
                if isinstance(value, nengo.Network):
                    to_process.append(value)

    def _scan_standard_lists(self, net):
        to_process = [net]
        while len(to_process) > 0:
            net = to_process.pop()
            for i, subnet in enumerate(net.networks):
                self._process_candidate(
                    subnet, f'{self._unique_name_map[net]}.networks[{i}]')
                to_process.append(subnet)
            for i, ens in enumerate(net.ensembles):
                self._process_candidate(
                    ens, f'{self._unique_name_map[net]}.ensembles[{i}]')
            for i, node in enumerate(net.nodes):
                self._process_candidate(
                    node, f'{self._unique_name_map[net]}.nodes[{i}]')

    def _process_candidate(self, obj, unique_name):
        if obj in self:
            return

        for base in type(obj).__mro__:
            if base in self.valid_types:
                self._unique_name_map[obj] = unique_name
                self._type_map[obj] = self.valid_types[base]
                id_key = self._get_id(self.valid_types[base], unique_name)
                self._reverse_map[id_key] = obj
                return

    def _get_id(self, type_name, unique_name):
        return ':'.join((self.prefix, type_name, unique_name))

    def __contains__(self, key):
        return key in self._type_map and key in self._unique_name_map

    def __getitem__(self, key):
        return self._get_id(self._type_map[key], self._unique_name_map[key])

    def reverse_lookup(self, id_key):
        return self._reverse_map[id_key]
