"""
Methods for creating experiment function call summaries.

Main method is writeSummary()
"""

import sys
from os import path
import inspect
from warnings import warn
from textwrap import dedent

__author__ = 'Marc Schulder'


# def _getCallingFunction():
#     curframe = inspect.currentframe()
#     try:
#         outerframes = inspect.getouterframes(curframe, 3)
#         # for f in outerframes[2]:
#         #     print f
#         parentframe, _, _, parentname, _, _ = outerframes[2]
#         print parentname, parentframe
#         #print parentframe.__dict__.itervalues()
#
#         frm = inspect.stack()[1]
#         mod = inspect.getmodule(frm[0])
#         print '[%s] %s' % (mod.__name__, frm)
#         return
#     finally:
#         del curframe


def writeSummary(func, outputDir, *args):
    """
    Write a summary of a given function.
    The function to be summarized must be provided as func.
    Example: To summarise foo() and save it to the subdir "summaries", call writeSummary(foo, 'summaries/')
    :param func: Reference to function to write the summary about. Required for extraction of docstring.
    :param outputDir:
    :param args:
    :return:
    """
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
    
    for i, block in enumerate(args):
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
            for j, line in enumerate(blocklines):
                if j == 0:
                    summary.append('{0}: {1}'.format(head, line))
                else:
                    summary.append('{0}{1}'.format(indentstr, line))
            summary.append('')
        else:
            warn("Unexpected format in args[{0}] of getSummary: {1}".format(i, block))

    # Return summary as a single string
    text = '\n'.join(summary)
    text = text.strip('\n')  # get rid of trailing newlines
    return text