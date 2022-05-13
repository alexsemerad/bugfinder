#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import unittest
from bugfinder import BugFinder


# * ── Test Bug Finder
class TestBugFinder(unittest.TestCase):

    # Provided Input
    def test_standard_input(self):
        bug_finder = BugFinder("tests/standard/bug.txt", "tests/standard/landscape.txt", True)
        result = bug_finder.parse_landscape()
        self.assertEqual(result, 3)

    # Modified Input, replacing whitespace with random ASCII characters
    def test_noisy_background(self):
        bug_finder = BugFinder("tests/noise/bug.txt", "tests/noise/landscape.txt", True)
        result = bug_finder.parse_landscape()
        self.assertEqual(result, 3)

    # Bugs may have overlapping Characters, see Explanation "Additional Parameters" in Bugfinder.py
    def test_avoid_overlapping_off(self):
        bug_finder = BugFinder("tests/overlapping/bug.txt", "tests/overlapping/landscape.txt", True)
        result = bug_finder.parse_landscape()
        self.assertEqual(result, 6)

    # Bugs shall not overlap, see Explanation "Additional Parameters" in Bugfinder.py
    def test_avoid_overlapping_on(self):
        bug_finder = BugFinder("tests/overlapping/bug.txt", "tests/overlapping/landscape.txt")
        result = bug_finder.parse_landscape()
        self.assertEqual(result, 9)

    # Large Input // See Line 293 & 490
    def test_insectus_maximus(self):
        bug_finder = BugFinder("tests/big/bug.txt", "tests/big/landscape.txt", True)
        result = bug_finder.parse_landscape()
        self.assertEqual(result, 2)


if __name__ == "__main__":
    unittest.main()
