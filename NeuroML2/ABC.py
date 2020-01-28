from neuromllite import Network, Cell, Population, Synapse, RectangularRegion, RandomLayout 
from neuromllite import Projection, RandomConnectivity, OneToOneConnector, Simulation, InputSource, Input

from neuromllite.NetworkGenerator import check_to_generate_or_run
from neuromllite.sweep.ParameterSweep import *

import sys


def generate():
    
    dt = 0.1
    simtime = 1
    
    ################################################################################
    ###   Build new network

    net = Network(id='ABC')
    net.notes = 'Example of simplified network'
    
    net.parameters = { 'A_input': 1}

    cellInput = Cell(id='a_input', lems_source_file='PNL.xml')
    net.cells.append(cellInput)

    cellA = Cell(id='a', lems_source_file='PNL.xml')
    net.cells.append(cellA)
    cellB = Cell(id='b', lems_source_file='PNL.xml')
    net.cells.append(cellB)
    cellC = Cell(id='c', lems_source_file='PNL.xml')
    net.cells.append(cellC)

    rsDL = Synapse(id='rsDL', neuroml2_source_file='inputs.nml')
    net.synapses.append(rsDL)

    r1 = RectangularRegion(id='region1', x=0,y=0,z=0,width=1000,height=100,depth=1000)
    net.regions.append(r1)


    pAin = Population(id='A_input', 
                    size='1', 
                    component=cellInput.id, 
                    properties={'color':'0.2 0.2 0.2', 'radius':3},
                    random_layout = RandomLayout(region=r1.id))
    net.populations.append(pAin)

    pA = Population(id='A', 
                    size='1', 
                    component=cellA.id, 
                    properties={'color':'0 0.9 0', 'radius':5},
                    random_layout = RandomLayout(region=r1.id))
    net.populations.append(pA)

    pB = Population(id='B', 
                    size='1', 
                    component=cellB.id, 
                    properties={'color':'.9 0 0', 'radius':5},
                    random_layout = RandomLayout(region=r1.id))
    net.populations.append(pB)
    
    pC = Population(id='C', 
                    size='1', 
                    component=cellC.id, 
                    properties={'color':'0.7 0 0', 'radius':5},
                    random_layout = RandomLayout(region=r1.id))
    net.populations.append(pC)
    
    silentDLin = Synapse(id='silentSyn_proj_input', neuroml2_source_file='inputs.nml')
    net.synapses.append(silentDLin)
    net.projections.append(Projection(id='proj_input',
                                      presynaptic=pA.id, 
                                      postsynaptic=pB.id,
                                      synapse=rsDL.id,
                                      pre_synapse=silentDLin.id,
                                      type='continuousProjection',
                                      weight='A_input',
                                      random_connectivity=RandomConnectivity(probability=1)))
    
    silentDL0 = Synapse(id='silentSyn_proj0', neuroml2_source_file='inputs.nml')
    net.synapses.append(silentDL0)
    net.projections.append(Projection(id='proj0',
                                      presynaptic=pAin.id, 
                                      postsynaptic=pA.id,
                                      synapse=rsDL.id,
                                      pre_synapse=silentDL0.id,
                                      type='continuousProjection',
                                      weight=1,
                                      random_connectivity=RandomConnectivity(probability=1)))
    
    silentDL1 = Synapse(id='silentSyn_proj1', neuroml2_source_file='inputs.nml')
    net.synapses.append(silentDL1)
    net.projections.append(Projection(id='proj1',
                                      presynaptic=pA.id, 
                                      postsynaptic=pC.id,
                                      synapse=rsDL.id,
                                      pre_synapse=silentDL1.id,
                                      type='continuousProjection',
                                      weight=1,
                                      random_connectivity=RandomConnectivity(probability=1)))
    

    new_file = net.to_json_file('%s.json'%net.id)


    ################################################################################
    ###   Build Simulation object & save as JSON

    sim = Simulation(id='Sim%s'%net.id,
                     network=new_file,
                     duration=simtime,
                     dt=dt,
                     seed= 123,
                     recordVariables={'OUTPUT':{'all':'*'},'INPUT':{'all':'*'}})

    sim.to_json_file()
    
    return sim, net



if __name__ == "__main__":


    sim, net = generate()

    ################################################################################
    ###   Run in some simulators

    import sys

    check_to_generate_or_run(sys.argv, sim)

