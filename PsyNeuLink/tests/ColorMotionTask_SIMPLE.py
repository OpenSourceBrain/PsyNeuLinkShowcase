from psyneulink import *

optimal_color_control = 1
optimal_motion_control = .5

color_input = ProcessingMechanism(name='Color',
                                  function=Linear(slope=optimal_color_control))
motion_input = ProcessingMechanism(name='Motion',
                                  function=Linear(slope=optimal_motion_control))
decision = DDM(name='Decision',
               function=DriftDiffusionAnalytical(
                       starting_point=0,
                       noise=0.5,
                       t0=0.2,
                       threshold=0.45),
               output_ports=[DDM_OUTPUT.PROBABILITY_UPPER_THRESHOLD, DDM_OUTPUT.RESPONSE_TIME],
               )

c = Composition(name='ColorMotion Task')
c.add_linear_processing_pathway([color_input, decision])
c.add_linear_processing_pathway([motion_input, decision])

c.show_graph()
#c.show_graph(show_node_structure=ALL)

stimuli = {color_input: [0,1,0],
              motion_input: [1,0,1]}

# c.run(inputs=stimuli)
# print (c.results)
print (dir(c))
print('--------')
print (c.json_summary)

base_fname = __file__.replace('.py', '')
with open(f'{base_fname}.json', 'w') as outfi:
    outfi.write(c.json_summary)


