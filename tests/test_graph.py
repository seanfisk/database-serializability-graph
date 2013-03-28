import os
import unittest

from serial_graph.graph import _find_conflicts


def open_fixture_file(basename):
    return open(os.path.join(os.path.dirname(__file__), 'fixtures', basename))


class TestConflicts(unittest.TestCase):
    def test_schedule_1(self):
        self.assertEqual(_find_conflicts(open_fixture_file('schedule1')),
                         (set([1, 2, 3]),
                          set([(1, 2, 'Z'), (3, 1, 'X'), (3, 2, 'Y')])))

    def test_schedule_2(self):
        self.assertEqual(_find_conflicts(open_fixture_file('schedule2')),
                         (set([1, 2, 3]),
                          set([(3, 1, 'X'), (1, 2, 'Z'), (2, 3, 'Y'),
                               (3, 2, 'Y')])))

    def test_schedule_3(self):
        self.assertEqual(_find_conflicts(open_fixture_file('schedule3')),
                         (set([1, 2, 3]), set()))
