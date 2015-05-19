# SAUSAGE: Semi-Adaptable User Suite for Advanced Generation of Experiments

A collection of methods to support a workflow for batch experiments in Python.

Tested for Python 2.7, should be compatible with 3.x.

## Introduction
The following scripts were developed to create a convenient way of setting up and running batches of different script configurations.
`batchcall.py` helps you to easily run a custom series of configurations from the console without having to expressly define the access.
`summary.py` lets each configuration create a semi-automatic summary of the configuration settings.

## Example: Batch Call
Imagine we are trying out different methods for determining whether someone is a witch. We have create a file `witchExperiment.py` and written a handful of different methods to determine witchiness, such as `isFlammable(person)`, `isEqualWeight(person, item)`. The methods require that you generate a `person` object beforehand and `compareWeight` also expects an item. To take care of the different preparation, we define two run methods:
```python
from batchcall import runExperimentScriptCall

def runExperiment1():
    witch = loadPerson('woman.data')
    isWitch = isFlammable(witch)
    print("Is a witch:", isWitch)

def runExperiment2a():
    witch = loadPerson('woman.data')
    items = loadItemList('thingsForBuildingBridges.txt')
    for item in items:
        if isEqualWeight(witch, item):
            print(item, "indicates this is a witch")

def runExperiment2b():
    witch = loadPerson('woman.data')
    items = loadItemList('floatingThings.txt')
    for item in items:
        if item != 'wood' and isEqualWeight(witch, item):
            print(item, "indicates this is a witch")

def main(args):
    runExperimentScriptCall(args, moduleName=__name__)

if __name__ == '__main__':
    main(sys.argv)
```
You can see that we have prepared the two experiments, including two alternative configurations for experiment 2, and let the main method call the batch call function.
Now we can call
```bash
$ python witchExperiment.py all
```
from the console to run all experiments at once or 
```bash
$ python witchExperiment.py 2a 2b
```
to only run the variations of experiment 2.

If you want to know which experiments are available, you simply do not provide any arguments:
```bash
$ python witchExperiment.py
USAGE: python witchExperiment.py EXPERIMENT_ID [EXPERIMENT_ID ...]
       Provide one more experiment IDs to run the respective experiments.
       To run all experiments, provide the argument 'all'.
AVAILABLE EXPERIMENT IDS: 1, 2a, 2b
```

As you can see, `runExperimentScriptCall()` figured out by itself which methods are experiments and linked the IDs to them. It does this by looking for any function in the main module (i.e. your script file) that starts with `runExperiment` and takes the rest of the name as its ID.

If you'd prefer your experiments to have more specific names, you could call them `runExperimentFlammable`, `runExperimentWeightBridge`, etc. In that case, the IDs would be _Flammable_ and _WeightBridge_.

If you would like to name your run methods differently, e.g. _testWitch_, you can do so by adding the parameter funcNamestart:
```python
def main(args):
    runExperimentScriptCall(args, moduleName=__name__, funcNamestart='testWitch')
```

## Example: Summary
**To do**
