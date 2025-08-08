"""
Festival Schedule Generator
===========================

A Python-based solution for the Demcon "Festival Schedule Generator" challenge.
This tool automatically assigns shows to the minimum number of stages required so that no overlapping shows occur on the same stage.

------------------------------------------------------
Project Description:
------------------------------------------------------
This project reads a list of shows (with start and end times) from a file or standard input,
then uses an efficient greedy scheduling algorithm to determine the fewest stages required
to host them without overlaps. It outputs both the total number of stages needed and
detailed stage assignments.

Key Features:
- Reads input in the format: <name> <start> <end>
- Treats end times as inclusive.
- Calculates optimal stage allocation.
- Outputs in both input order and per-stage order.
- Works from either a text file or standard input.

------------------------------------------------------
Setup Instructions (GitHub Repository):
------------------------------------------------------
1. Install Python 3.8+.
2. Create a new repository on GitHub and clone it locally.
3. Add this script as festival_schedule_generator.py.
4. Create input.txt with your show schedule.
5. Commit and push the files to GitHub.

------------------------------------------------------
How to Run:
------------------------------------------------------
- From a file:
    python festival_schedule_generator.py input.txt
- From standard input:
    cat input.txt | python festival_schedule_generator.py

------------------------------------------------------
Logic Overview:
------------------------------------------------------
1. Parse input into (name, start, end) tuples.
2. Sort shows by start time.
3. Use a min-heap to track when stages become free.
4. Assign shows to the earliest available stage or create a new one.
5. Print results.

------------------------------------------------------
Files in This Project:
------------------------------------------------------
- festival_schedule_generator.py: Main code.
- input.txt: Example input.
- README.md: Documentation.
- requirements.txt: Dependencies (empty).
"""

import sys
import heapq
from collections import defaultdict
from typing import List, Tuple


def parse_lines(lines: List[str]) -> List[Tuple[str, int, int]]:
    """Parses each line of the input into a (name, start, end) tuple."""
    shows = []
    for lineno, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split()
        if len(parts) < 3:
            raise ValueError(f"Line {lineno}: expected 3 tokens, got: {line!r}")
        name = parts[0]
        try:
            start = int(parts[1])
            end = int(parts[2])
        except ValueError:
            raise ValueError(f"Line {lineno}: start/end must be integers: {line!r}")
        if end < start:
            raise ValueError(f"Line {lineno}: end < start: {line!r}")
        shows.append((name, start, end))
    return shows


def assign_stages(shows: List[Tuple[str, int, int]]):
    """
    Assign shows to the minimum number of stages using a greedy algorithm with a min-heap.
    End times are treated as inclusive, so a new show starting at 'end' is considered overlapping.
    """
    shows_sorted = sorted(shows, key=lambda s: (s[1], s[2]))
    occupied = []
    free_stage_ids = []
    next_stage_id = 1
    assignments = {}
    stage_timelines = defaultdict(list)

    for name, start, end in shows_sorted:
        # Free up stages that are done before the current show's start
        while occupied and occupied[0][0] < start:
            freed_end, freed_stage = heapq.heappop(occupied)
            heapq.heappush(free_stage_ids, freed_stage)

        # Assign a freed stage if available, else create a new one
        if free_stage_ids:
            stage = heapq.heappop(free_stage_ids)
        else:
            stage = next_stage_id
            next_stage_id += 1

        assignments[name] = stage
        stage_timelines[stage].append((name, start, end))
        heapq.heappush(occupied, (end, stage))

    num_stages = next_stage_id - 1
    return assignments, stage_timelines, num_stages


def print_schedule(assignments, stage_timelines, num_stages, original_order=None):
    """Prints the total stages, assignments in input order, and per-stage timelines."""
    print(f"Total stages required: {num_stages}\n")
    if original_order:
        print("Assignments in input order:")
        for name, start, end in original_order:
            stage = assignments[name]
            print(f"  {name}: {start} - {end}  --> Stage {stage}")
        print()
    print("Per-stage timelines:")
    for stage in sorted(stage_timelines.keys()):
        print(f"Stage {stage}:")
        for name, start, end in sorted(stage_timelines[stage], key=lambda t: t[1]):
            print(f"  {name}: {start} - {end}")
        print()


def main(argv):
    if len(argv) > 1:
        path = argv[1]
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    else:
        lines = sys.stdin.read().strip().splitlines()

    shows = parse_lines(lines)
    assignments, stage_timelines, num_stages = assign_stages(shows)
    print_schedule(assignments, stage_timelines, num_stages, original_order=shows)


if __name__ == '__main__':
    main(sys.argv)
