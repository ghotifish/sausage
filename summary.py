"""
Methods for creating experiment function call summaries.

Main method is writeSummary()
"""

import sys
from os import path
import inspect
from textwrap import dedent

__author__ = 'Marc Schulder'


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

    return

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
            print "WARNING: Unexpected format in args of getSummary"

    # Return summary as a single string
    text = '\n'.join(summary)
    text = text.strip('\n')  # get rid of trailing newlines
    return text