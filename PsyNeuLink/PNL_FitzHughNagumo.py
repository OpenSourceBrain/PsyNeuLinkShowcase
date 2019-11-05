import psyneulink as pnl
import sys

fhn = pnl.FitzHughNagumoIntegrator(
    a_v=0.7,
    a_w=0.7,
    b_v=0.8,
    b_w=0.8,
    initial_v=-1.2,
    initial_w=-0.6,
    time_step_size=0.001,
)

syn1_flat = pnl.TransferMechanism(name='syn1_flat', function=pnl.Exponential)

fn_pop1 = pnl.IntegratorMechanism(name='fnPop1', function=fhn)
fn_pop2 = pnl.IntegratorMechanism(name='fnPop2', function=fhn)

composition = pnl.Composition()
composition.add_linear_processing_pathway([fn_pop1, syn1_flat, fn_pop2])

sys.stderr.write(composition.json_summary)
