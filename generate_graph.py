#!/usr/bin/env python

from __future__ import print_function
import re
import argparse


class Operation(object):
    """Represent an operation."""
    def __init__(self, is_write, transaction_number, data_item):
        """:param is_write: Whether the operation is a write
        :type is_write: :class:`bool`
        :param transaction_number: Index of transaction
        :type transaction_number: :class:`int`
        :param data_item: Data item accessed
        :type data_item: :class:`str`
        """
        self.is_write = is_write
        self.transaction_number = transaction_number
        self.data_item = data_item

arg_parser = argparse.ArgumentParser(
    description='Generate serializabilty graphs.')
arg_parser.add_argument(
    'input_file', metavar='INPUT_FILE', help='File containing schedule.',
    type=argparse.FileType('r'))
arg_parser.add_argument(
    'output_file', metavar='OUTPUT_FILE',
    help='Output image file to contain the graph.',
    type=argparse.FileType('w'))
args = arg_parser.parse_args()

line_re = re.compile(r'([rw])(\d+)\((\w+)\)$')

operations = []

for line_no, line in enumerate(args.input_file):
    line_match = line_re.match(line.rstrip())
    if line_match is None:
        raise SystemExit(
            'Incorrect input file syntax on line {0}.'.format(line_no))
    operations.append(Operation(line_match.group(1) == 'w',
                                int(line_match.group(2)),
                                line_match.group(3)))
args.input_file.close()

conflicts = []

for i in xrange(len(operations) - 1):
    op1 = operations[i]
    for j in xrange(i + 1, len(operations)):
        op2 = operations[j]
        if ((op1.is_write or op2.is_write) and
                op1.transaction_number != op2.transaction_number and
                op1.data_item == op2.data_item):
            conflicts.append((i, j))

print(conflicts)
