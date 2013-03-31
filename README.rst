.. image:: https://secure.travis-ci.org/seanfisk/cpg-islands.png
   :target: https://secure.travis-ci.org/seanfisk/cpg-islands

==========================================
 Database Serializability Graph Generator
==========================================

Generate database serializability graphs from an operation schedule using Graphviz! This program is not intended to be a full-fledged project; it was just a fun program for my database internals course.

A command-line interface and graphical user interface are included.

Running
=======

`Python 2.7`_ and Graphviz_ are necessary to run both the CLI and the GUI, and PySide_ is necessary for the GUI. Install as needed.

First, pull down the code::

    git clone https://github.com/seanfisk/database-serializability-graph.git
    cd database-serializability-graph

Next, install the Python package requirements::

    pip install pydot

Run the CLI in the following way (bash):

.. code-block:: bash

    PYTHONPATH=$PWD serial_graph/cli.py

Run the GUI in the following way (bash):

.. code-block:: bash

    PYTHONPATH=$PWD serial_graph/gui.py

Entering Schedules
==================

Schedules use a defined format which can easily be learned by looking at some examples. Please see the examples in the ``tests/fixtures`` directory.

.. _Python 2.7: http://python.org/download/releases/2.7.3/
.. _Graphviz: http://graphviz.org/
.. _PySide: http://pyside.org/
