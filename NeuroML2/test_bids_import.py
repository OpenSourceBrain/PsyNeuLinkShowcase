import psyneulink as pnl

net_id = 'ABC'

with open('%s.bids-mdf.json'%net_id, 'r') as infile:
    json = infile.read()
    
print(json)


with open('%s.bids-mdf.py'%net_id, 'w') as outfi:
    outfi.write(pnl.generate_script_from_json(json))
    outfi.write('\n\n%s.show_graph()'%net_id)
    
