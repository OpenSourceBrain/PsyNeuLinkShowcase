import matplotlib.pyplot as plt
import numpy as np
import psyneulink as pnl

# This implements the model by Cohen, J. D., & Huston, T. A. (1994). Progress in the use of interactive
# models for understanding attention and performance. In C. Umilta & M. Moscovitch(Eds.),
# AttentionandperformanceXV(pp.453-456). Cam- bridge, MA: MIT Press.
# The model aims to capute top-down effects of selective attention and the bottom-up effects of attentional capture.

# Define Variables ----------------------------------------------------------------------------------------------------
import psyneulink.core.components.functions.transferfunctions

rate = 0.1          # modified from the original code from 0.01 to 0.1
inhibition = -2.0   # lateral inhibition
bias = 4.0          # bias is positive since Logistic equation has - sing already implemented
threshold = 0.55    # modified from thr original code from 0.6 to 0.55 because incongruent condition won't reach 0.6
settle_trials = 50  # cycles until model settles

# Create mechanisms ---------------------------------------------------------------------------------------------------
#   Linear input units, colors: ('red', 'green'), words: ('RED','GREEN')
colors_input_layer = pnl.TransferMechanism(
    size=3,
    function=psyneulink.core.components.functions.transferfunctions.Linear,
    name='COLORS_INPUT'
)

words_input_layer = pnl.TransferMechanism(
    size=3,
    function=psyneulink.core.components.functions.transferfunctions.Linear,
    name='WORDS_INPUT'
)

task_input_layer = pnl.TransferMechanism(
    size=2,
    function=psyneulink.core.components.functions.transferfunctions.Linear,
    name='TASK_INPUT'
)

#   Task layer, tasks: ('name the color', 'read the word')
task_layer = pnl.RecurrentTransferMechanism(
    size=2,
    function=psyneulink.core.components.functions.transferfunctions.Logistic(),
    hetero=-2,
    integrator_mode=True,
    integration_rate=0.1,
    name='TASK'
)

#   Hidden layer units, colors: ('red','green') words: ('RED','GREEN')
colors_hidden_layer = pnl.RecurrentTransferMechanism(
    size=3,
    function=psyneulink.core.components.functions.transferfunctions.Logistic(x_0=4.0),
    integrator_mode=True,
    hetero=-2.0,
    # noise=pnl.NormalDist(mean=0.0, standard_deviation=.0).function,
    integration_rate=0.1,  # cohen-huston text says 0.01
    name='COLORS HIDDEN'
)

words_hidden_layer = pnl.RecurrentTransferMechanism(
    size=3,
    function=psyneulink.core.components.functions.transferfunctions.Logistic(x_0=4.0),
    hetero=-2,
    integrator_mode=True,
    # noise=pnl.NormalDist(mean=0.0, standard_deviation=.05).function,
    integration_rate=0.1,
    name='WORDS HIDDEN'
)
#   Response layer, responses: ('red', 'green'): RecurrentTransferMechanism for self inhibition matrix
response_layer = pnl.RecurrentTransferMechanism(
    size=2,
    function=psyneulink.core.components.functions.transferfunctions.Logistic(),
    hetero=-2.0,
    integrator_mode=True,
    integration_rate=0.1,
    name='RESPONSE'
)

# Log mechanisms ------------------------------------------------------------------------------------------------------
task_layer.set_log_conditions('value')
colors_hidden_layer.set_log_conditions('value')
words_hidden_layer.set_log_conditions('value')
response_layer.set_log_conditions('value')
# Connect mechanisms --------------------------------------------------------------------------------------------------
# (note that response layer projections are set to all zero first for initialization

color_input_weights = pnl.MappingProjection(
    matrix=np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0]
    ])
)

word_input_weights = pnl.MappingProjection(
    matrix=np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0]
    ])
)

task_input_weights = pnl.MappingProjection(
    matrix=np.array([
        [1.0, 0.0],
        [0.0, 1.0]
    ])
)

color_task_weights = pnl.MappingProjection(
    matrix=np.array([
        [4.0, 0.0],
        [4.0, 0.0],
        [4.0, 0.0]
    ])
)

task_color_weights = pnl.MappingProjection(
    matrix=np.array([
        [4.0, 4.0, 4.0],
        [0.0, 0.0, 0.0]
    ])
)

word_task_weights = pnl.MappingProjection(
    matrix=np.array([
        [0.0, 4.0],
        [0.0, 4.0],
        [0.0, 4.0]
    ])
)

task_word_weights = pnl.MappingProjection(
    matrix=np.array([
        [0.0, 0.0, 0.0],
        [4.0, 4.0, 4.0]
    ])
)

response_color_weights = pnl.MappingProjection(
    matrix=np.array([
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0]
    ])
)

response_word_weights = pnl.MappingProjection(
    matrix=np.array([
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0]
    ])
)

color_response_weights = pnl.MappingProjection(
    matrix=np.array([
        [1.5, 0.0],
        [0.0, 1.5],
        [0.0, 0.0]
    ])
)
word_response_weights = pnl.MappingProjection(
    matrix=np.array([
        [2.5, 0.0],
        [0.0, 2.5],
        [0.0, 0.0]
    ])
)
#
# Create pathways -----------------------------------------------------------------------------------------------------
color_response_process_1 = pnl.Process(
    pathway=[
        colors_input_layer,
        color_input_weights,
        colors_hidden_layer,
        color_response_weights,
        response_layer,
    ],
    name='COLORS_RESPONSE_PROCESS_1'
)

color_response_process_2 = pnl.Process(
    pathway=[
        response_layer,
        response_color_weights,
        colors_hidden_layer
    ],
    name='COLORS_RESPONSE_PROCESS_2'
)

word_response_process_1 = pnl.Process(
    pathway=[
        words_input_layer,
        word_input_weights,
        words_hidden_layer,
        word_response_weights,
        response_layer
    ],
    name='WORDS_RESPONSE_PROCESS_1'
)

word_response_process_2 = pnl.Process(
    pathway=[
        response_layer,
        response_word_weights,
        words_hidden_layer
    ],
    name='WORDS_RESPONSE_PROCESS_2'
)

task_color_response_process_1 = pnl.Process(
    pathway=[
        task_input_layer,
        task_input_weights,
        task_layer,
        task_color_weights,
        colors_hidden_layer])

task_color_response_process_2 = pnl.Process(
    pathway=[
        colors_hidden_layer,
        color_task_weights,
        task_layer])

task_word_response_process_1 = pnl.Process(
    pathway=[
        task_input_layer,
        task_layer,
        task_word_weights,
        words_hidden_layer])

task_word_response_process_2 = pnl.Process(
    pathway=[
        words_hidden_layer,
        word_task_weights,
        task_layer])


# Create system -------------------------------------------------------------------------------------------------------
Bidirectional_Stroop = pnl.System(
    processes=[
        color_response_process_1,
        word_response_process_1,
        task_color_response_process_1,
        task_word_response_process_1,
        color_response_process_2,
        word_response_process_2,
        task_color_response_process_2,
        task_word_response_process_2
    ],
    reinitialize_mechanisms_when=pnl.Never(),
    name='Bidirectional_Stroop_SYSTEM'
)
response_layer._add_system(Bidirectional_Stroop, pnl.TERMINAL)
Bidirectional_Stroop.terminal_mechanisms.append(response_layer)

input_dict = {colors_input_layer: [0, 0, 0],
              words_input_layer: [0, 0, 0],
              task_input_layer: [0, 1]}
print("\n\n\n\n")
print(Bidirectional_Stroop.run(inputs=input_dict))

for node in Bidirectional_Stroop.mechanisms:
    print(node.name, " Value: ", node.get_output_values(Bidirectional_Stroop))
# # LOGGING:
# colors_hidden_layer.set_log_conditions('value')
# words_hidden_layer.set_log_conditions('value')
#
# Bidirectional_Stroop.show()
# Bidirectional_Stroop.show_graph(show_dimensions=pnl.ALL)  # ,show_mechanism_structure=pnl.VALUES) # Uncomment to show graph of the system
#
# # Create threshold function -------------------------------------------------------------------------------------------
#
#
# def pass_threshold(response_layer, thresh):
#     results1 = response_layer.output_ports.values[0][0]  # red response
#     results2 = response_layer.output_ports.values[0][1]  # green response
#     if results1 >= thresh or results2 >= thresh:
#         return True
#     return False
#
#
# terminate_trial = {
#     pnl.TimeScale.TRIAL: pnl.While(pass_threshold, response_layer, threshold)
# }
#
# # Create test trials function -----------------------------------------------------------------------------------------
# # a BLUE word input is [1,0] to words_input_layer and GREEN word is [0,1]
# # a blue color input is [1,0] to colors_input_layer and green color is [0,1]
# # a color-naming trial is [1,0] to task_layer and a word-reading trial is [0,1]
#
#
# def trial_dict(red_color, green_color, neutral_color, red_word, green_word, neutral_word, CN, WR):
#
#     trialdict = {
#         colors_input_layer: [red_color, green_color, neutral_color],
#         words_input_layer: [red_word, green_word, neutral_word],
#         task_input_layer: [CN, WR]
#     }
#     return trialdict
#
#
# # Define initialization trials separately
# WR_initialize_input = trial_dict(0, 0, 0, 0, 0, 0, 0, 1)
# CN_initialize_input = trial_dict(0, 0, 0, 0, 0, 0, 1, 0)
#
# CN_incongruent_trial_input = trial_dict(1, 0, 0, 0, 1, 0, 1, 0)  # red_color, green color, red_word, green word, CN, WR
# CN_congruent_trial_input = trial_dict(1, 0, 0, 1, 0, 0, 1, 0)  # red_color, green color, red_word, green word, CN, WR
# CN_control_trial_input = trial_dict(1, 0, 0, 0, 0, 0, 1, 0)  # red_color, green color, red_word, green word, CN, WR
#
# WR_congruent_trial_input = trial_dict(1, 0, 0, 1, 0, 0, 0, 1)  # red_color, green color, red_word, green word, CN, WR
# WR_incongruent_trial_input = trial_dict(1, 0, 0, 0, 1, 0, 0, 1)  # red_color, green color, red_word, green word, CN, WR
# WR_control_trial_input = trial_dict(0, 0, 0, 1, 0, 0, 0, 1)  # red_color, green color, red_word, green word, CN, WR
#
# Stimulus = [[CN_initialize_input, CN_control_trial_input],
#             [CN_initialize_input, CN_incongruent_trial_input],
#             [CN_initialize_input, CN_congruent_trial_input]]
#
# Stimulus2 = [[WR_initialize_input, WR_control_trial_input],
#              [WR_initialize_input, WR_incongruent_trial_input],
#              [WR_initialize_input, WR_control_trial_input]]
#
# conditions = 3
# response_all = []
# response_all2 = []
#
# # Run color naming trials ----------------------------------------------------------------------------------------------
# for cond in range(conditions):
#     response_color_weights = pnl.MappingProjection(
#         matrix=np.array([
#             [0.0, 0.0, 0.0],
#             [0.0, 0.0, 0.0]
#         ])
#     )
#     response_word_weights = pnl.MappingProjection(
#         matrix=np.array([
#             [0.0, 0.0, 0.0],
#             [0.0, 0.0, 0.0]
#         ])
#     )
#
#     Bidirectional_Stroop.run(inputs=Stimulus[cond][0], num_trials=settle_trials)
#     response_color_weights = pnl.MappingProjection(
#         matrix=np.array([
#             [1.5, 0.0, 0.0],
#             [0.0, 1.5, 0.0]
#         ])
#     )
#     response_word_weights = pnl.MappingProjection(
#         matrix=np.array([
#             [2.5, 0.0, 0.0],
#             [0.0, 2.5, 0.0]
#         ])
#     )
#     Bidirectional_Stroop.run(inputs=Stimulus[cond][1], termination_processing=terminate_trial)
#
#     # Store values from run -----------------------------------------------------------------------------------------------
#     r = response_layer.log.nparray_dictionary('value')       # Log response output from special logistic function
#     rr = r['value']
#     n_r = rr.shape[0]
#     rrr = rr.reshape(n_r, 2)
#     response_all.append(rrr)  # .shape[0])
#     response_all2.append(rrr.shape[0])
#
#     # Clear log & reinitialize ----------------------------------------------------------------------------------------
#     response_layer.log.clear_entries(delete_entry=False)
#     colors_hidden_layer.log.clear_entries(delete_entry=False)
#     words_hidden_layer.log.clear_entries(delete_entry=False)
#     task_layer.log.clear_entries(delete_entry=False)
#     colors_hidden_layer.reinitialize([[0, 0, 0]])
#     words_hidden_layer.reinitialize([[0, 0, 0]])
#     response_layer.reinitialize([[0, 0]])
#     task_layer.reinitialize([[0, 0]])
#     print('response_all: ', response_all)
#
# # Run color naming trials ----------------------------------------------------------------------------------------------
# response_all3 = []
# response_all4 = []
# for cond in range(conditions):
#     response_color_weights = pnl.MappingProjection(
#         matrix=np.array([
#             [0.0, 0.0, 0.0],
#             [0.0, 0.0, 0.0]
#         ])
#     )
#     response_word_weights = pnl.MappingProjection(
#         matrix=np.array([
#             [0.0, 0.0, 0.0],
#             [0.0, 0.0, 0.0]
#         ])
#     )
#
#     Bidirectional_Stroop.run(inputs=Stimulus2[cond][0], num_trials=settle_trials)
#     response_color_weights = pnl.MappingProjection(
#         matrix=np.array([
#             [1.5, 0.0, 0.0],
#             [0.0, 1.5, 0.0]
#         ])
#     )
#     response_word_weights = pnl.MappingProjection(
#         matrix=np.array([
#             [2.5, 0.0, 0.0],
#             [0.0, 2.5, 0.0]
#         ])
#     )
#     Bidirectional_Stroop.run(inputs=Stimulus2[cond][1], termination_processing=terminate_trial)
#
#     # Store values from run -----------------------------------------------------------------------------------------------
#     r2 = response_layer.log.nparray_dictionary('value')       # Log response output from special logistic function
#     rr2 = r2['value']
#     n_r2 = rr2.shape[0]
#     rrr2 = rr2.reshape(n_r2, 2)
#     response_all3.append(rrr2)  # .shape[0])
#     response_all4.append(rrr2.shape[0])
#
#     # Clear log & reinitialize ----------------------------------------------------------------------------------------
#     response_layer.log.clear_entries(delete_entry=False)
#     colors_hidden_layer.log.clear_entries(delete_entry=False)
#     words_hidden_layer.log.clear_entries(delete_entry=False)
#     task_layer.log.clear_entries(delete_entry=False)
#     colors_hidden_layer.reinitialize([[0, 0, 0]])
#     words_hidden_layer.reinitialize([[0, 0, 0]])
#     response_layer.reinitialize([[0, 0]])
#     task_layer.reinitialize([[0, 0]])
#     print('response_all: ', response_all)
#
#
# # Plot results --------------------------------------------------------------------------------------------------------
# # First, plot response layer activity for whole run
# plt.figure()
# # color naming plot
# plt.plot(response_all[0])
# plt.plot(response_all[1])
# plt.plot(response_all[2])
# # word reading plot
# plt.plot(response_all3[0])
# plt.plot(response_all3[1])
# plt.plot(response_all3[2])
# plt.show()
# # Second, plot regression plot
# # regression
# reg = np.dot(response_all2, 5) + 115
# reg2 = np.dot(response_all4, 5) + 115
# plt.figure()
#
# plt.plot(reg, '-s')  # plot color naming
# plt.plot(reg2, '-or')  # plot word reading
# plt.title('GRAIN MODEL with bidirectional weights')
# plt.legend(['color naming', 'word reading'])
# plt.xticks(np.arange(3), ('control', 'incongruent', 'congruent'))
# plt.ylabel('reaction time in ms')
# plt.show()
