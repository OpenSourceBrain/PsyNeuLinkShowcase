import psyneulink as pnl

#my_encoder.show_graph(show_controller=True)

lin = pnl.Linear(slope=3)
lin.name='TripleTheNumber'
print (lin.json_summary)
print (dir(lin))

print(lin.execute(5))

adder = pnl.ProcessingMechanism(name='Tripler',size=2,function=lin)

print(adder)

print(adder.execute([1,2]))

#print (adder.json_summary)

print('Done!')