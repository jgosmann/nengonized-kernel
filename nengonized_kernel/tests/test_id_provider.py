import gc

import nengo
import pytest
import weakref

from nengonized_kernel.id_provider import IdProvider


def test_provides_id_for_nengo_objects_based_on_locals_dict():
    with nengo.Network() as model:
        with nengo.Network() as subnetwork:
            node = nengo.Node(0.)
        ens = nengo.Ensemble(10, 1)

    id_provider = IdProvider(model, locals(), prefix='no')

    assert id_provider[model] == 'no:Network:model'
    assert id_provider[subnetwork] == 'no:Network:subnetwork'
    assert id_provider[node] == 'no:Node:node'
    assert id_provider[ens] == 'no:Ensemble:ens'


def test_does_not_keep_strong_references():
    with nengo.Network() as model:
        ens = nengo.Ensemble(10, 1)

    model_ref = weakref.ref(model)
    ens_ref = weakref.ref(ens)

    id_provider = IdProvider(model, {'model': model, 'ens': ens})
    del model, ens

    assert model_ref() is None
    assert ens_ref() is None


def test_provides_id_for_network_attributes():
    with nengo.Network() as model:
        model.ens = nengo.Ensemble(10, 1)
        with nengo.Network() as model.subnetwork:
            model.subnetwork.ens = nengo.Ensemble(10, 1)

    id_provider = IdProvider(model, {'model': model}, prefix='no')

    assert id_provider[model.ens] == 'no:Ensemble:model.ens'
    assert id_provider[model.subnetwork] == 'no:Network:model.subnetwork'
    assert id_provider[model.subnetwork.ens] == (
            'no:Ensemble:model.subnetwork.ens')


def test_provides_id_from_standard_lists():
    with nengo.Network() as model:
        ens = nengo.Ensemble(10, 1)
        node = nengo.Node(0.)
        net = nengo.Network()

    id_provider = IdProvider(model, {'model': model}, prefix='no')

    assert id_provider[ens] == 'no:Ensemble:model.ensembles[0]'
    assert id_provider[node] == 'no:Node:model.nodes[0]'
    assert id_provider[net] == 'no:Network:model.networks[0]'


def test_provides_reverse_mapping():
    with nengo.Network() as model:
        ens = nengo.Ensemble(10, 1)

    id_provider = IdProvider(model, {'model': model}, prefix='no')

    assert id_provider.reverse_lookup(id_provider[ens]) is ens
