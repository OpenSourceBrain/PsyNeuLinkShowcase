import psyneulink as pnl
import psyneulink.core.components.functions.transferfunctions


# Construct the Mechanisms:
input_layer = pnl.ProcessingMechanism(name='InputLayer',size=5)
hidden_layer = pnl.ProcessingMechanism(size=2, function=pnl.Logistic)
output_layer = pnl.ProcessingMechanism(size=5, function=pnl.Logistic)

# Construct the Composition:
my_encoder = pnl.Composition()
my_encoder.add_linear_processing_pathway([input_layer, hidden_layer, output_layer])

print(my_encoder)

#my_encoder.show_graph(show_controller=True)

print (input_layer.json_summary)

print('Done!')