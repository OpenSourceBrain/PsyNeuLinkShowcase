set -e

python ABC.py -jnml
python ABC.py -pnl
jnml LEMS_SimABC.xml -graph
jnml LEMS_SimABC.xml -nogui

python ABCD.py -jnml
python ABCD.py -pnl
jnml LEMS_SimABCD.xml -graph
jnml LEMS_SimABCD.xml -nogui

python test_bids_import.py 

python McCP.py -jnml
python McCP.py -pnl
jnml LEMS_SimMcCPNet.xml -graph
jnml LEMS_SimMcCPNet.xml -nogui

jnml LEMS_FitzHughNagumo.xml -nogui
jnml LEMS_FitzHughNagumo.xml -graph

python FN.py -jnml
python FN.py -pnl
python run_pnl_FN.py