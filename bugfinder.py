#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


# fmt: off
__author__  = "Alexander Semerad"
__date__    = "12.05.2022"
__status__  = "Development"
__version__ = "0.1"
# fmt: on


""" ── Trayport Test: BugFinder
    - Goal:
        Seach a text file for bugs and print the number of their occurence.

    - First Thought:
        Some people, when confronted with a problem, think
        "I know, I'll use regular expressions." Now they have two problems.

    - Current Approach:
        1. Both inputs, Landscape and Bug, are converted into list of lists.
        2. We iterate over the Landscape searching for an indication of a bug.
            This is, the "head" of the bug (first line), matches with a sublist,
            of same length, in the current row of the landscape.
        3. Given the form of the bug (known length of columns and rows), we extract
            this shape from the landscape.
        4. if the extracted shape matches, we found a bug!

    - Additional Parameters:
        a. the Class features one more addtional attribute: ignore_overlap.
            Dedicated to the following scenario where it might seem that a given
            landscape features 2 bugs, but where these two instances share common
            characters.

            Landscape:               Bug Shape:
                      | | |                    | |
                      #####                    ###
                      | | |                    | |

            To avoid this and only count one bug, the coordinates (row, col)
            are stored in a set if a bug is found. These coordinations are then
            skipped while the parsing of the remaining landscape."""


# * ── Bug Finder
class BugFinder(object):
    def __init__(self, bug_filepath, landscape_filepath, ignore_overlap=False):
        self.count = 0
        self.bug = self.open_file(bug_filepath)
        self.landscape = self.open_file(landscape_filepath)
        self.coordinates = set()
        self.ignore_overlap = ignore_overlap

    # ── Convert ASCII Text File to Grid (List of Lists)
    def open_file(self, file_path):
        """Reads file and iterates over each line, converting it into a list,
        while excluding any newline ('\n') character. All 'line lists' are
        collected into one big list, forming a list of lists."""

        grid = []
        with open(file_path, "r") as f:
            for line in f:
                grid.append(list(filter(lambda char: char != "\n", line)))

        return grid

    # ── Ignore Whitespace
    def ignore_whitespace(self, src, target, nested=False):
        # If Nested (list of lists), flatten it to a single list.
        if nested:
            src = [item for lst in src for item in lst]
            target = [item for lst in target for item in lst]

        for index, item in enumerate(src):
            if item != " ":  # Skip Whitespaces in Src (Bug)!
                if item != target[index]:  # Break / Return False if remaining characters don't match.
                    return False

        return True

    # ── Match Bug
    def match_bug(self, start_row_num, start_col_num):
        """Given the indication of a possible bug, it extracts the characters
        from the landscape given the shape (rows and columns) of the bug.
        Once extracted, it compares if the extraction matches the bug."""

        # Ignore Col out of Range ↓
        if (start_row_num + len(self.bug)) > (len(self.landscape)):
            return False

        # Init Vars. // Grid refers to the extracted rows/cols from the landscape
        grid, coordinates = [], set()

        # Extract Bug Shape from Landscape
        for bug_row_num, bug_row in enumerate(self.bug):

            # Define Current Row, Col of the Landscape
            grid_row_num = start_row_num + bug_row_num
            grid_col_num = start_col_num + len(bug_row)

            # Ignore Row out of Range →
            if (grid_col_num) > (len(self.landscape[grid_row_num])):
                return False

            # Append extracted sublist from landscape to Grid
            grid.append(self.landscape[grid_row_num][start_col_num:grid_col_num])

            # Store Coordinates
            for col in range(start_col_num, grid_col_num):
                coordinates.add((grid_row_num, col))

        # return Findings
        # if self.bug == grid:
        if self.ignore_whitespace(self.bug, grid, nested=True):
            if self.ignore_overlap:
                self.coordinates.update(coordinates)
            return True
        return False

    # ── Parse Landscape Searching for Bug
    def parse_landscape(self):
        """Parses through the Landscape searching for a possible bug by iterating
        over each line, creating a substring which is compared to the first line of the
        bug."""

        # Resetting Count
        self.count = 0
        self.coordinates = set()

        # Iterate over Landscape Rows ↓
        for row_num, row in enumerate(self.landscape):
            row_length = len(row)

            # Iterate over Landscape Cols →
            for col_num in range(row_length):

                # Define The Col. List Slice to Compare
                bug_head = self.bug[0]
                col_slice_end = col_num + len(bug_head)

                # Ignore List Slices out of Range
                if col_slice_end > row_length:
                    continue

                # Optional: Ignore already parsed coordinates
                if self.ignore_overlap:
                    if (row_num, col_num) in self.coordinates:
                        continue

                # Find the first matching row of Bug in Landscape
                # if row[col_num:col_slice_end] == bug_head:
                if self.ignore_whitespace(bug_head, row[col_num:col_slice_end]):
                    if self.match_bug(row_num, col_num):
                        self.count += 1

        return self.count


# * ── Run Script
if __name__ == "__main__":
    bug_finder = BugFinder("input/bug.txt", "input/landscape.txt", True)
    result = bug_finder.parse_landscape()

    print("Count: {}".format(result))
