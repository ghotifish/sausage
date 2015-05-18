"""
Methods to support the running of batch experiments in Python.

Main method is runExperimentScriptCall()
"""

from __future__ import print_function
import sys
from os import path
import re
import inspect
from textwrap import dedent

__author__ = 'Marc Schulder'

DEFAULT_FUNC_NAMESTART = "runExperiment"


# # # Functions for automated function calls # # #
def _natural_key(string_):
    """
    Sort key that provides natural sorting for numbers in strings.
    Usage: sorted(mylist, key=natural_key)
    Source: http://www.codinghorror.com/blog/archives/001018.html
    """
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]


def _is_mod_function(mod, func):
    """
    Check whether something is a function and belongs to the given module.
    Source: http://stackoverflow.com/a/1107150
    """
    return inspect.isfunction(func) and inspect.getmodule(func) == mod


def _list_functions(mod):
    """
    List all functions of a given module
    Source: http://stackoverflow.com/questions/1106840/find-functions-explicitly-defined-in-a-module-python
    """
    return [func for func in mod.__dict__.itervalues() if _is_mod_function(mod, func)]


def runExperimentScriptCall(args=None, moduleName='__main__', funcNamestart=DEFAULT_FUNC_NAMESTART, verbose=True):
    """
    Run set of experiment function by dynamically interpreting script call arguments.
    This function is a wrapper to run the entire function selection process.

    Experiment functions  must start with the string defined by funcNamestart.
    The script call argument required to execute a function is the function name WITHOUT the funcNamestart beginning
    (e.g. if funcNamestart='foo', the function foo3a() is called if args[1:] contains '3a').
    :param args: Arguments of the script call. First entry must be path of script file, rest are arguments for call.
                 If args is None (default), sys.argv is used.
    :param funcNamestart: String with which all callable functions must start.
                          This part of the function name will be dropped from the argument which calls the function

    :param moduleName: Name of module containing the experiment scripts.
                       Specify if experiment functions are not in main module.
    :param verbose: Name of module containing the experiment scripts.
    """
    if args is None:
        args = sys.argv

    experiments = getExperimentFunctions(moduleName, funcNamestart=funcNamestart)
    if len(args) <= 1:
        print(getExperimentUsage(experiments, scriptname=args[0]))
    else:
        runExperimentSelection(experiments, args[1:], verbose=verbose)


def runExperimentSelection(experiments, args=None, verbose=True):
    """
    Run a set of experiments.
    Usually args should be sys.argv[1:] (to avoid the script name)
    If arg is None, an empty list or contains the entry "all", all experiments will be run.
    :param experiments: A dict mapping experiment names (strings) to their run functions.
                        The run functions should require no further arguments
    :param args: List of experiment names that should be run.
    :return:
    """
    ALL_MODE = 'all'
    DEFAULT_MODE = ALL_MODE
    modes = list()
    if args is not None and len(args) >= 1:
        for arg in args:
            mode = arg.lower()
            if mode == ALL_MODE:
                modes = [ALL_MODE]
                break
            else:
                modes.append(mode)
    else:
        modes = [DEFAULT_MODE]

    for mode in modes:
        if mode in experiments:
            if verbose:
                print("Running experiment", mode)
            experiments[mode]()
        elif mode == 'all':
            if verbose:
                print("Running all experiments")
            for thismode, experiment in sorted(experiments.items()):
                if verbose:
                    print("Running experiment", thismode)
                experiment()
        else:
            if verbose:
                print("Experiment {0} does not exist.".format(mode))

    if verbose:
        if len(modes) == 1 and 'all' not in modes:
            print("Finished running experiment")
        else:
            print("Finished running all experiments")


def getExperimentUsage(experiments, scriptname=None):
    """
    Get default info for experiment ID based script calls.
    :param experiments: Dictionary of experiment functions as returned by getExperimentFunctions()
    :param scriptname: Name of the python script. If None (default), name is taken from path
    :return: A multiline string containing the usage information.
    """
    if scriptname is None:
        scriptname = path.split(sys.argv[0])[1]

    expString = ', '.join(sorted(experiments, key=_natural_key))

    usage = list()
    usage.append("USAGE: python {0} EXPERIMENT_ID [EXPERIMENT_ID ...]".format(scriptname))
    usage.append("       Provide one more experiment IDs to run the respective experiments.")
    usage.append("       To run all experiments, provide the argument 'all'.")
    usage.append("AVAILABLE EXPERIMENT IDS: {0}".format(expString))
    return '\n'.join(usage)


def getExperimentFunctions(moduleName, funcNamestart=DEFAULT_FUNC_NAMESTART):
    """
    Get all experiment functions that are defined in the given module.
    :param moduleName: Name of the module. Use __name__ to apply to the module you are calling this from.
    :param funcNamestart: The mandatory beginning of each function name. This part will be cut from the dict key.
    :return: Dict mapping function name (sans funcNamestart) to function.
    """
    if funcNamestart is None:
        funcNamestart = ''
    genericLength = len(funcNamestart)
    functions = _list_functions(sys.modules[moduleName])
    return {func.__name__[genericLength:]: func for func in functions if func.__name__.startswith(funcNamestart)}


# # # Functions for summary generation # # #
def writeSummary(func, outputDir, *args):
    summary = getSummary(func, *args)

    # Determine file name
    expname = func.func_name
    if expname.lower().startswith('run'):
        expname = expname[3:]
    if expname[0].isupper():
        expname = expname[0].lower() + expname[1:]
    filename = 'info_{0}.txt'.format(expname)

    # Write to file
    filepath = path.join(outputDir, filename)
    with open(filepath, 'w') as w:
        w.write(summary)


def getSummary(func, *args):
    summary = list()

    # Process doc string
    doc = func.func_doc
    doc = dedent(doc)
    doc = doc.strip('\n')
    summary.append(doc)
    summary.append('')

    # Process data information
    scriptdir, scriptname = path.split(sys.argv[0])
    summary.append('=============== Data ===============')
    summary.append('Created by: {0}'.format(scriptname))
    summary.append('            {0}()'.format(func.func_name))
    summary.append('')

    for block in args:
        if isinstance(block, basestring):
            summary.append(block)
        elif len(block) == 0:
            summary.append(block)
        elif len(block) >= 2:
            # Flatten list
            blocklines = list()
            for item in block[1:]:
                if isinstance(item, basestring):
                    blocklines.append(item)
                else:
                    blocklines.extend(item)
            # Write lines
            head = block[0]
            indentstr = ' '*(len(head)+2)
            for i, line in enumerate(blocklines):
                if i == 0:
                    summary.append('{0}: {1}'.format(head, line))
                else:
                    summary.append('{0}{1}'.format(indentstr, line))
            summary.append('')
        else:
            print("WARNING: Unexpected format in args of getSummary")

    # Return summary as a single string
    text = '\n'.join(summary)
    text = text.strip('\n')  # get rid of trailing newlines
    return text