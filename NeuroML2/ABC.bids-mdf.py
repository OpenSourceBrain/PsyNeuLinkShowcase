import ABC
import psyneulink as pnl

ABC = pnl.Composition(name='ABC')

A_0 = pnl.TransferMechanism(name='A_0', function=pnl.Linear(intercept=2, slope=5))
A_input_0 = pnl.TransferMechanism(name='A_input_0', function=pnl.Linear(default_variable=0))
B_0 = pnl.TransferMechanism(name='B_0', function=pnl.Logistic)
C_0 = pnl.TransferMechanism(name='C_0', function=pnl.Exponential)

ABC.add_node(A_0)
ABC.add_node(A_input_0)
ABC.add_node(B_0)
ABC.add_node(C_0)

ABC.add_projection(projection=pnl.MappingProjection(name='Edge A_0 to B_0'), sender=A_0, receiver=B_0)
ABC.add_projection(projection=pnl.MappingProjection(name='Edge A_input_0 to A_0'), sender=A_input_0, receiver=A_0)
ABC.add_projection(projection=pnl.MappingProjection(name='Edge A_0 to C_0'), sender=A_0, receiver=C_0)

ABC.show_graph()