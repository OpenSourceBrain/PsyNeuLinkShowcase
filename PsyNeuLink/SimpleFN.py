import psyneulink as pnl
import sys

time_step_size=0.1

fhn = pnl.FitzHughNagumoIntegrator(
    initial_v=-1,
    initial_w=0,
    time_step_size=time_step_size,
)


fn = pnl.IntegratorMechanism(name='fn', function=fhn)

comp = pnl.Composition(name='comp')
comp.add_linear_processing_pathway([fn])

comp.run(inputs={fn:1}, log=True, num_trials=1000)


print('Finished running model')

print(comp.results)

base_fname = __file__.replace('.py', '')
with open(f'{base_fname}.json', 'w') as outfi:
    outfi.write(comp.json_summary)

with open(f'{base_fname}.converted.py', 'w') as outfi:
    outfi.write(pnl.generate_script_from_json(comp.json_summary))
    outfi.write('\ncomp.show_graph()')

for node in comp.nodes:
    print(f'=== {node} {node.name}: {node.parameters.value.get(comp)}')
    
import matplotlib.pyplot as plt

def generate_time_array(node, context='comp', param='value'):
    return [entry.time.trial for entry in getattr(node.parameters, param).log[context]]

def generate_value_array(node, index, context='comp', param='value'):
    return [float(entry.value[index]) for entry in getattr(node.parameters, param).log[context]]

for node in comp.nodes:
    print(f'>> {node}: {generate_time_array(node)}')
    
    for i in [0,1,2]:
        print(f'>> {node}: {generate_value_array(node,i)}')
    

fig, axes = plt.subplots()
for i in [0,1]:
    x_values = {node: generate_time_array(node) for node in comp.nodes}
    y_values = {node: generate_value_array(node, i) for node in comp.nodes}

    fout = open('SimpleFN_%i.dat'%i,'w')
    for index in range(len(x_values[node])):
        #                                            1000 to convert ms to s
        fout.write('%s\t%s\n'%(x_values[node][index]*time_step_size/1000.0, \
                               y_values[node][index]))
    fout.close()

    for node in comp.nodes:
        axes.plot(
            x_values[node],
            y_values[node],
            label=f'Value of {i} {node.name}, {node.function.__class__.__name__}'
        )

axes.set_xlabel('Trial')
axes.legend()
plt.show()