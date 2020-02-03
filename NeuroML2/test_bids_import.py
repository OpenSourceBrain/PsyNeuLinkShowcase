import psyneulink as pnl

net_ids = ['ABC', 'ABCD']

for net_id in net_ids:
    conv_json_filename = '%s.bids-mdf.json'%net_id
    with open(conv_json_filename, 'r') as infile:
        json = infile.read()

    #print(json)
    py_filename = '%s.bids-mdf.py'%net_id
    with open(py_filename, 'w') as outfi:
        outfi.write(pnl.generate_script_from_json(json))
        outfi.write('\n\n%s.show_graph()'%net_id)
        
    print('Written JSON file: %s and python to load it: %s'%(conv_json_filename, py_filename))
    
