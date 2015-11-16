#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Methods for creating experiment function call summaries.

Main method is writeSummary()
"""

import sys
from os import path
from inspect import getdoc
from warnings import warn

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
    
    # Get doc string
    doc = getdoc(func)
    if doc is not None:
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
                if isinstance(item, basestring):  # Add string
                    item = item.strip()
                    if '\n' in item:  # String is single line
                        itemlines = [s.strip() for s in item.split('\n')]
                        blocklines.extend(itemlines)
                    else:  # String is multiline
                        blocklines.append(item)
                else:  # Add iterables
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
