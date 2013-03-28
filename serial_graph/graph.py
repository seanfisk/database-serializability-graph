""":mod:`serial_graph.graph` --- Find schedule conflicts and graph them
"""

import re

import pygraphviz


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

LINE_RE = re.compile(r'([rw])(\d+)\((\w+)\)$')
"""Line recognition regular expression."""


class ParseError(Exception):
    def __init__(self, line_number):
        self.line_number = line_number

    def __str__(self):
        return 'Incorrect input file syntax on line {0}.'.format(
            self.line_number)


def _find_conflicts(schedule_file):
    """Find conflicts in a schedule.

    :param schedule_file: File object containing the schedule
    :type schedule_file: :class:`file`
    :return: tuple of ``(transactions, conflicts)``
    :rtype: :class:`tuple`
    """
    # Parse the input file, creating representations of operations and
    # transactions.
    operations = []
    transactions = set()

    for line_index, line in enumerate(schedule_file):
        line_match = LINE_RE.match(line.rstrip())
        if line_match is None:
            # Lines in a file are always numbered starting at 1. But Python
            # always starts indices at 0.
            raise ParseError(line_index + 1)
        is_write = line_match.group(1) == 'w'
        transaction_number = int(line_match.group(2))
        data_item = line_match.group(3)
        operations.append(Operation(is_write, transaction_number, data_item))
        transactions.add(transaction_number)

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

    return (transactions, conflicts)


def generate_serializability_graph(schedule_file):
    """Find conflicts in a schedule.

    :param schedule_file: File object containing the schedule
    :type schedule_file: :class:`file`
    :return: generated pygraphviz AGraph object
    :rtype: :class:`pygraphviz.AGraph`
    """
    # Find conflicts.
    transactions, conflicts = _find_conflicts(schedule_file)

    # Create the graph.
    graph = pygraphviz.AGraph(strict=False, directed=True)

    # Output graph nodes (transactions).
    for transaction in transactions:
        graph.add_node(transaction, label='T{0}'.format(transaction))

    # Output graph edges (conflicts).
    for op1_num, op2_num, data_item in conflicts:
        graph.add_edge(op1_num, op2_num, label=data_item)

    # Use `dot' program for layout.
    graph.layout(prog='dot')

    # Don't write out the result here this allows the driver programs to either
    # write to a file with a path or a file descriptor in memory.

    return graph
