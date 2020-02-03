import psyneulink as pnl
import ABCD

ABCD = pnl.Composition(name='ABCD')

A_0 = pnl.TransferMechanism(name='A_0')
A_input_0 = pnl.TransferMechanism(name='A_input_0')
B_0 = pnl.TransferMechanism(name='B_0')
C_0 = pnl.TransferMechanism(name='C_0')
D_0 = pnl.TransferMechanism(name='D_0')

ABCD.add_node(A_0)
ABCD.add_node(A_input_0)
ABCD.add_node(B_0)
ABCD.add_node(C_0)
ABCD.add_node(D_0)

ABCD.add_projection(projection=pnl.MappingProjection(name='Edge A_0 to B_0'), sender=A_0, receiver=B_0)
ABCD.add_projection(projection=pnl.MappingProjection(name='Edge A_input_0 to A_0'), sender=A_input_0, receiver=A_0)
ABCD.add_projection(projection=pnl.MappingProjection(name='Edge A_0 to C_0'), sender=A_0, receiver=C_0)
ABCD.add_projection(projection=pnl.MappingProjection(name='Edge B_0 to D_0'), sender=B_0, receiver=D_0)
ABCD.add_projection(projection=pnl.MappingProjection(name='Edge C_0 to D_0'), sender=C_0, receiver=D_0)

ABCD.show_graph()