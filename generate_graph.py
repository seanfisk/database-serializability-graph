#!/usr/bin/env python

from __future__ import print_function
import re
import argparse

import pydot


# Storage class.
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

# Parse arguments.
arg_parser = argparse.ArgumentParser(
    description='Generate serializabilty graphs.')
arg_parser.add_argument(
    'input_file', metavar='INPUT_FILE', help='File containing schedule.',
    type=argparse.FileType('r'))
arg_parser.add_argument(
    'output_file', metavar='OUTPUT_FILE',
    help='Output image file to contain the graph.')
args = arg_parser.parse_args()

# Line recognition regular expression.
line_re = re.compile(r'([rw])(\d+)\((\w+)\)$')

# Parse the input file, creating representations of operations and
# transactions.
operations = []
transactions = set()

for line_no, line in enumerate(args.input_file):
    line_match = line_re.match(line.rstrip())
    if line_match is None:
        raise SystemExit(
            'Incorrect input file syntax on line {0}.'.format(line_no))
    is_write = line_match.group(1) == 'w'
    transaction_number = int(line_match.group(2))
    data_item = line_match.group(3)
    operations.append(Operation(is_write, transaction_number, data_item))
    transactions.add(transaction_number)

# Done with the input file.
args.input_file.close()

# Calculate conflicts.
conflicts = set()

for i in xrange(len(operations) - 1):
    op1 = operations[i]
    for j in xrange(i + 1, len(operations)):
        op2 = operations[j]
        if ((op1.is_write or op2.is_write) and
                op1.transaction_number != op2.transaction_number and
                op1.data_item == op2.data_item):
            conflicts.add((op1.transaction_number,
                           op2.transaction_number,
                           op1.data_item))


# Output the graph.
graph = pydot.Dot(graph_type='digraph')
node_names = {}

# Output graph nodes (transactions).
for transaction in transactions:
    node = pydot.Node('T{0}'.format(transaction))
    node_names[transaction] = node
    graph.add_node(node)

# Output graph edges (conflicts).
for op1_num, op2_num, data_item in conflicts:
    graph.add_edge(pydot.Edge(node_names[op1_num],
                              node_names[op2_num],
                              label=data_item))

# Write out the final product.
graph.write_png(args.output_file)
