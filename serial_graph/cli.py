#!/usr/bin/env python

import sys
import argparse

from serial_graph.graph import generate_serializability_graph


def main(argv):
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

    graph = generate_serializability_graph(args.input_file)

    # Done with the input file.
    args.input_file.close()

    graph.draw(args.output_file)

if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
