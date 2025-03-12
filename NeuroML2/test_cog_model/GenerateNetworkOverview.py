from neuromllite.NetworkGenerator import check_to_generate_or_run
from neuromllite import Simulation

from neuromllite import Network, Population, Projection, Cell, Synapse, InputSource, Input
from neuromllite import RandomConnectivity, RectangularRegion, RelativeLayout

import sys

# This function generates the overview of the network using neuromllite
def internal_connections(pops):
    for pre in pops:
        for post in pops:

            weight = W[pops.index(post)][pops.index(pre)]
            print('Connection %s -> %s weight: %s'%(pre.id,
            post.id, weight))
            if weight!=0:
                syn = syns[pre.id]
                standard_projection(pre, post, syn, weight)
                                                    
def standard_projection(pre, post, syn, weight):
    
    net.projections.append(Projection(id='proj_%s_%s'%(pre.id,post.id),
                                                    presynaptic=pre.id,
                                                    postsynaptic=post.id,
                                                    synapse=syn,
                                                    type='continuousProjection',
                                                    delay=0,
                                                    weight=weight,
                                                    random_connectivity=RandomConnectivity(probability=1)))
    
    
# Build the network
net = Network(id='BioCog')
net.notes = 'A simple network'

net.parameters = { 'wee':      1.0,
                   'wei':      1.0,
                   'wie':      -8,
                   'wii':      -3}  

r0 = RectangularRegion(id='PosteriorCortex', x=0,y=0,z=0,width=1000,height=100,depth=1000)
net.regions.append(r0)
r1 = RectangularRegion(id='FrontalCortex', x=0,y=0,z=0,width=1000,height=100,depth=1000)
net.regions.append(r1)
r2 = RectangularRegion(id='Striatum', x=0,y=100,z=0,width=1000,height=100,depth=1000)
net.regions.append(r2)

exc_cell = Cell(id='Exc', lems_source_file='../WC_Parameters.xml')
inh_cell = Cell(id='Inh', lems_source_file='../RateBased.xml') #  hack to include this file too.  

net.cells.append(exc_cell)
net.cells.append(inh_cell)

pc_pop = Population(id='PC', 
                     size=1, 
                     component=exc_cell.id, 
                     properties={'color': '.0 .92 .92','radius':10},
                     relative_layout = RelativeLayout(region=r0.id,x=-20,y=0,z=0))
net.populations.append(pc_pop)

fc_pop = Population(id='FC', 
                     size=1, 
                     component=exc_cell.id, 
                     properties={'color': '.92 .0 .92','radius':10},
                     relative_layout = RelativeLayout(region=r1.id,x=-20,y=0,z=0))
net.populations.append(fc_pop)

go_pop = Population(id='Go', 
                     size=1, 
                     component=inh_cell.id, 
                     properties={'color': '.92 .92 .92','radius':10},
                     relative_layout = RelativeLayout(region=r2.id,x=20,y=0,z=0))

nogo_pop = Population(id='NoGo', 
                     size=1, 
                     component=inh_cell.id, 
                     properties={'color': '0 1 0.4','radius':10},
                     relative_layout = RelativeLayout(region=r2.id,x=20,y=0,z=0))

net.populations.append(go_pop)
net.populations.append(nogo_pop)

thalamus_pop = Population(id='Thalamus', 
                     size=1, 
                     component=exc_cell.id, 
                     properties={'color': '.92 .92 0','radius':10})
net.populations.append(thalamus_pop)

gpe_pop = Population(id='GPe', 
                     size=1, 
                     component=exc_cell.id, 
                     properties={'color': '.5 .5 .92','radius':10})
net.populations.append(gpe_pop)

snr_pop = Population(id='SNr', 
                     size=1, 
                     component=exc_cell.id, 
                     properties={'color': '1 1 0.4','radius':10})
                     
net.populations.append(snr_pop)


exc_syn = Synapse(id='rsExc', lems_source_file='WC_Parameters.xml')
inh_syn = Synapse(id='rsInh', lems_source_file='RateBased.xml')
net.synapses.append(exc_syn)
net.synapses.append(inh_syn)

standard_projection(pc_pop, fc_pop, exc_syn.id, 1)
standard_projection(pc_pop, go_pop, exc_syn.id, 1)
standard_projection(pc_pop, nogo_pop, exc_syn.id, 1)
standard_projection(fc_pop, pc_pop, exc_syn.id, 1)
standard_projection(fc_pop, go_pop, exc_syn.id, 1)
standard_projection(fc_pop, nogo_pop, exc_syn.id, 1)

standard_projection(thalamus_pop, nogo_pop, exc_syn.id, 1)
standard_projection(thalamus_pop, fc_pop, exc_syn.id, 1)
standard_projection(fc_pop, thalamus_pop, exc_syn.id, 1)

standard_projection(nogo_pop, gpe_pop, inh_syn.id, -1)
standard_projection(gpe_pop, snr_pop, inh_syn.id, -1)
standard_projection(go_pop, snr_pop, inh_syn.id, -1)
standard_projection(snr_pop, thalamus_pop, inh_syn.id, -1)


# Add offset inputs

net.parameters['exc_input'] = '0nA'
net.parameters['inh_input'] = '0nA'
net.parameters['input_delay'] = '20ms'
net.parameters['input_duration'] = '60ms'

#net.parameters['scaling'] = '1nA'
'''
input_source_e = InputSource(id='Exc_in',
                             neuroml2_input='PulseGenerator',
                             parameters={'amplitude':'exc_input', 'delay':'input_delay', 'duration':'input_duration'})
net.input_sources.append(input_source_e)
net.inputs.append(Input(id='Exc_stim',
                        input_source=input_source_e.id,
                        population=pc_pop.id,
                        percentage=100))
                        
input_source_i = InputSource(id='Inh_in',
                             neuroml2_input='PulseGenerator',
                             parameters={'amplitude':'inh_input', 'delay':'input_delay', 'duration':'input_duration'})
net.input_sources.append(input_source_i)
net.inputs.append(Input(id='Inh_stim',
                        input_source=input_source_i.id,
                        population=go_pop.id,
                        percentage=100))'''

# Save to JSON format
new_file = net.to_json_file('%s.json'%net.id)

sim = Simulation(id='Sim%s'%net.id,
                                    duration='100',
                                    dt='0.005',
                                    network=new_file,
                                    record_rates={'all':'*'})
                                    
sim.to_json_file('Sim%s.nmllite.json'%net.id)

check_to_generate_or_run(sys.argv,sim)
