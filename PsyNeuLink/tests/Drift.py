from psyneulink import *
import numpy as np

# Mechanisms
Input = TransferMechanism(name='Input')
#reward = TransferMechanism(output_ports=[RESULT, OUTPUT_MEAN, OUTPUT_VARIANCE],
#                               name='reward')
                               
Decision = DDM( function=DriftDiffusionAnalytical(
                    drift_rate=0.1,
                    starting_point=0.05,
                    threshold=0.2222,
                    noise=0.1,
                    t0=0.15),
                   name='Decision')

comp = Composition(name="MainComposition")
#comp.add_node(reward, required_roles=[NodeRole.OUTPUT])
comp.add_node(Decision, required_roles=[NodeRole.OUTPUT])


#comp.show_graph(show_node_structure=ALL)

task_execution_pathway = [Input, Decision]

comp.add_linear_processing_pathway(task_execution_pathway)

stim_list_dict = {
    Input: [0.5555, 0.123]
}
def record_trial(context):
    print('  ------------   Recording...')
    #print('  %s'%dir(context))
    #print('  %s'%context.execution_time)
    #print('    %s'%Decision.parameters)
    print('    %s'%Input.parameters)
    
comp.run(inputs=stim_list_dict,
    num_trials=10,
    call_after_trial=record_trial)

#comp.show_graph(show_node_structure=ALL)


'''
decision_process = Process(
    pathway=[
        task_execution_pathway
    ],
    name='DECISION PROCESS'
)

task = System(processes=[decision_process],
                  reinitialize_mechanisms_when=Never())

#print(Decision.execute([0]))



print('\nRunning model...')
task.run(
    inputs=[2],
    num_trials=10,
    call_after_trial=record_trial
)
print('\nModel run...')

print('Done')
print(Decision)'''



# comp.show_graph(show_model_based_optimizer=True)
# comp.run(inputs=stim_list_dict)
