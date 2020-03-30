import psyneulink as pnl

comp = pnl.Composition(name='comp')

fn = pnl.IntegratorMechanism(name='fn', function=pnl.FitzHughNagumoIntegrator(a_v=-0.3333333333333333, initial_v=-1, initial_w=0, initializer=[1.0], time_step_size=0.1, default_variable=[[0]]))

comp.add_node(fn)


comp.scheduler.add_condition(fn, pnl.Always())

comp.scheduler.termination_conds = {pnl.TimeScale.RUN: pnl.Never(), pnl.TimeScale.TRIAL: pnl.AllHaveRun()}
comp.show_graph()