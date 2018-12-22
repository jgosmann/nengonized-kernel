import nengo


with nengo.Network() as model:
    ens = nengo.Ensemble(10, 1, label="Ensemble")
