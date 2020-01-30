from neuromllite import Network, Cell, Population, Synapse, RectangularRegion, RandomLayout 
from neuromllite import Projection, RandomConnectivity, OneToOneConnector, Simulation, InputSource, Input

from neuromllite.NetworkGenerator import check_to_generate_or_run
from neuromllite.sweep.ParameterSweep import *

import sys


def generate():
    
    dt = 0.025
    simtime = 1000
    
    ################################################################################
    ###   Build new network

    net = Network(id='McCPNet')
    net.notes = 'Example of simplified McCulloch-Pitts based Network'
    

    net.parameters = { 'amp': 1.5,
                       'scale': 3}

    cell = Cell(id='mccp0', lems_source_file='McCPTest.xml')
    net.cells.append(cell)

    silentDL = Synapse(id='silentSyn_proj0', lems_source_file='McCPTest.xml')
    net.synapses.append(silentDL)
    rsDL = Synapse(id='rsDL', lems_source_file='McCPTest.xml')
    net.synapses.append(rsDL)


    r1 = RectangularRegion(id='region1', x=0,y=0,z=0,width=1000,height=100,depth=1000)
    net.regions.append(r1)


    p0 = Population(id='McCPpop0', 
                    size='1*scale', 
                    component=cell.id, 
                    properties={'color':'.9 0.9 0', 'radius':5},
                    random_layout = RandomLayout(region=r1.id))
    net.populations.append(p0)

    p1 = Population(id='McCPpop1', 
                    size='1*scale', 
                    component=cell.id, 
                    properties={'color':'.9 0 0.9', 'radius':5},
                    random_layout = RandomLayout(region=r1.id))
    net.populations.append(p1)
                    
    net.projections.append(Projection(id='proj0',
                                      presynaptic=p0.id, 
                                      postsynaptic=p1.id,
                                      synapse=rsDL.id,
                                      pre_synapse=silentDL.id,
                                      type='continuousProjection',
                                      weight='random()',
                                      random_connectivity=RandomConnectivity(probability=0.6)))

    '''
                                      
    
    net.synapses.append(Synapse(id='ampa', 
                                pynn_receptor_type='excitatory', 
                                pynn_synapse_type='curr_alpha', 
                                parameters={'tau_syn':0.1}))
                                
    
    net.projections.append(Projection(id='proj1',
                                      presynaptic=pEpoisson.id, 
                                      postsynaptic=pLNP.id,
                                      synapse='ampa',
                                      delay=0,
                                      weight='in_weight',
                                      random_connectivity=RandomConnectivity(probability=0.7)))'''

    input_source0 = InputSource(id='sg0', neuroml2_source_file='inputs.nml')
    net.input_sources.append(input_source0)
    input_source1 = InputSource(id='sg1', neuroml2_source_file='inputs.nml')
    net.input_sources.append(input_source1)

    for pop in [p0.id]:
        net.inputs.append(Input(id='stim0_%s'%pop,
                                input_source=input_source0.id,
                                population=pop,
                                percentage=60))
                                
        net.inputs.append(Input(id='stim1_%s'%pop,
                                input_source=input_source1.id,
                                population=pop,
                                percentage=60))
                                

    #print(net)
    #print(net.to_json())
    new_file = net.to_json_file('%s.json'%net.id)


    ################################################################################
    ###   Build Simulation object & save as JSON

    sim = Simulation(id='Sim%s'%net.id,
                     network=new_file,
                     duration=simtime,
                     dt=dt,
                     seed= 123,
                     recordVariables={'R':{'all':'*'},'ISyn':{'all':'*'}})

    sim.to_json_file()
    
    return sim, net



if __name__ == "__main__":


    sim, net = generate()

    ################################################################################
    ###   Run in some simulators

    import sys

    check_to_generate_or_run(sys.argv, sim)

