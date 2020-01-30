set -e

python ABC.py -jnml
python ABC.py -pnl
jnml LEMS_SimABC.xml -graph


python McCP.py -jnml
python McCP.py -pnl
jnml LEMS_SimMcCPNet.xml -graph

jnml LEMS_FitzHughNagumo.xml -nogui
jnml LEMS_FitzHughNagumo.xml -graph