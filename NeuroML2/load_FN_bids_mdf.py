import psyneulink as pnl

FN = pnl.Composition(name='FN')

FNpop_0 = pnl.IntegratorMechanism(name='FNpop_0', function=pnl.FitzHughNagumoIntegrator(a_v=-0.3333333333333333, d_v=1, initial_v=-1, initial_w=0))

FN.add_node(FNpop_0)
