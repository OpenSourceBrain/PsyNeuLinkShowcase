# Example of FitzHugh Nagumo network in NeuroML 

Simple example of network in NeuroML, which can potentially be mapped to the equivalent in PsyNeuLink

## Network:

![net](net1.gv.png)

Definition of network structure in NeuroML2:

[FitzHughNagumoNetwork.net.nml](FitzHughNagumoNetwork.net.nml)

Definition of simulation using LEMS Simulation:

[LEMS_FitzHughNagumo.xml](LEMS_FitzHughNagumo.xml)

Summary of structure in JSON (so called DLEMS, or distilled LEMS format):

[LEMS_FitzHughNagumo.json](LEMS_FitzHughNagumo.json)

## To run

### Use pyNeuroML

See https://github.com/NeuroML/pyNeuroML

```
    pynml LEMS_FitzHughNagumo.xml
```

### Use PyLEMS

See https://github.com/LEMS/pylems

```
    ...
```