import json
import os
import psyneulink as pnl
import subprocess

fname = "../NeuroML2/LEMS_FitzHughNagumo.json"
converted_json_fname = 'LEMS_FitzHughNagumo.converted.json'
converted_pnl_script_fname = 'LEMS_FitzHughNagumo.converted.py'


def filename_to_samedir_filename(f):
    return f"{os.path.abspath(os.path.dirname(__file__))}/{f}"


# assume above file is in the same directory as this file
with open(filename_to_samedir_filename(fname)) as input_file:
    lems_json = json.loads(input_file.read())

neuroml_to_pnl_name_mappings = {
    "synapses": "nodes",
    "populations": "nodes",
    "projections": "edges",

    "fnCell_flat": "FitzHughNagumoIntegrator",
    "simpleExponentialSynapse_flat": "Exponential"
}

pnl_to_neuroml_parameter_mapping = {
    "a_v": "a",
    "a_w": "a",
    "b_v": "b",
    "b_w": "b",
    "initial_v": "V0",
    "initial_w": "W0",
    "time_step_size": "TS",
}


def parse_synpop(data):
    parsed = {}

    try:
        data = data["synapse"]
    except KeyError:
        try:
            data = data["component"]
        except KeyError:
            return parsed

    parsed["name"] = data["name"]

    try:
        pnl_type = neuroml_to_pnl_name_mappings[data["type"]]
    except KeyError:
        pnl_type = data["type"]
    parsed["type"] = {
        "PNL": pnl_type,
        "generic": None
    }

    parsed["args"] = {}
    try:
        pnl_type = eval(f"pnl.{pnl_type}")
    except (SyntaxError, NameError, AttributeError):
        return

    for param_name, default in pnl_type.defaults.values(show_all=True).items():
        if param_name in pnl_to_neuroml_parameter_mapping:
            neuroml_name = pnl_to_neuroml_parameter_mapping[param_name]
        else:
            neuroml_name = param_name

        try:
            parsed["args"][param_name] = data["parameters"][neuroml_name]
        except KeyError:
            parsed["args"][param_name] = default

    return parsed


def parse_projection(data):
    # a projection in LEMS form appears to consist of two
    # projections
    # pre_population -> synapse -> post_population
    a = pnl.ProcessingMechanism(name=data['pre_population'])
    b = pnl.ProcessingMechanism(name=data['synapse'])
    c = pnl.ProcessingMechanism(name=data['post_population'])

    basic_json_proj_1 = pnl.MappingProjection(sender=a, receiver=b)._dict_summary
    basic_json_proj_2 = pnl.MappingProjection(sender=b, receiver=c)._dict_summary

    return basic_json_proj_1, basic_json_proj_2


def generate_shell_component_json_dict(pnl_class):
    return {
        "parameters": {},
        "type": {
            "PNL": pnl_class.__name__,
            "generic": None
        }
    }


converted_json = {
    "graphs": [
        {
            "name": "composition",
            "nodes": {},
            "edges": {},
            "parameters": {},
            "type": {
                "PNL": "Composition",
                "generic": "graph"
            }
        }
    ]
}
composition = converted_json["graphs"][0]

for name, synapse in lems_json["synapses"].items():
    # assume synapses correspond to transfer mechanisms
    node = generate_shell_component_json_dict(pnl.TransferMechanism)
    node.update({
        "name": name,
        'functions': [
            parse_synpop(synapse)
        ],
    })

    composition["nodes"][name] = node


for name, population in lems_json["populations"].items():
    # assume synapses correspond to transfer mechanisms
    node = generate_shell_component_json_dict(pnl.IntegratorMechanism)
    node.update({
        "name": name,
        'functions': [
            parse_synpop(population)
        ],
    })

    composition["nodes"][name] = node

for name, projection in lems_json["projections"].items():
    # unsure of any edge parameters in the original json
    for proj in parse_projection(projection):
        proj_name = proj['name']
        composition['edges'][proj_name] = proj

converted_json = json.dumps(
    converted_json,
    cls=pnl.PNLJSONEncoder,
    indent=4,
)

print(converted_json)

with open(filename_to_samedir_filename(converted_json_fname), 'w') as outfi:
    outfi.write(converted_json)

with open(filename_to_samedir_filename(converted_pnl_script_fname), 'w') as outfi:
    outfi.write(pnl.generate_script_from_json(converted_json))
    outfi.write('\ncomposition.show_graph()')

# make output py script easier to read using black
line_length = 80
subprocess.Popen(
    [
        'black',
        '-l',
        str(line_length),
        filename_to_samedir_filename(converted_pnl_script_fname)
    ]
)
