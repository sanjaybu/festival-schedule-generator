#!/usr/bin/env python3
"""
Festival Schedule Generator
===========================

A Python-based solution for the Demcon "Festival Schedule Generator" challenge.
This tool automatically assigns shows to the minimum number of stages required 
so that no overlapping shows occur on the same stage.

Author: Sanjay
Challenge: https://careersatdemcon.com/decode-demcon/challenge-festival-schedule-generator
"""

import sys
import heapq
from collections import defaultdict
from typing import List, Tuple, Dict, Optional


def parse_lines(lines: List[str]) -> List[Tuple[str, int, int]]:
    """
    Parses each line of the input into a (name, start, end) tuple.
    
    Args:
        lines: List of input lines to parse
        
    Returns:
        List of (show_name, start_time, end_time) tuples
        
    Raises:
        ValueError: If input format is invalid
    """
    shows = []
    for lineno, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        parts = line.split()
        if len(parts) < 3:
            raise ValueError(f"Line {lineno}: expected 3 tokens (name start end), got: {line!r}")
            
        name = parts[0]
        try:
            start = int(parts[1])
            end = int(parts[2])
        except ValueError:
            raise ValueError(f"Line {lineno}: start/end must be integers: {line!r}")
            
        if end < start:
            raise ValueError(f"Line {lineno}: end time ({end}) cannot be before start time ({start}): {line!r}")
            
        shows.append((name, start, end))
    
    return shows


def assign_stages(shows: List[Tuple[str, int, int]]) -> Tuple[Dict[str, int], Dict[int, List[Tuple[str, int, int]]], int]:
    """
    Assign shows to the minimum number of stages using a greedy algorithm with a min-heap.
    
    End times are treated as inclusive, meaning a show ending at time T conflicts 
    with a show starting at time T.
    
    Args:
        shows: List of (show_name, start_time, end_time) tuples
        
    Returns:
        Tuple of:
        - assignments: Dict mapping show names to stage numbers
        - stage_timelines: Dict mapping stage numbers to lists of shows
        - num_stages: Total number of stages required
    """
    if not shows:
        return {}, {}, 0
    
    # Sort shows by start time, then by end time to break ties
    shows_sorted = sorted(shows, key=lambda s: (s[1], s[2]))
    
    # Min-heap to track when stages become free: (end_time, stage_id)
    occupied = []
    # Min-heap of available stage IDs
    free_stage_ids = []
    next_stage_id = 1
    
    assignments = {}
    stage_timelines = defaultdict(list)

    for name, start, end in shows_sorted:
        # Free up stages that finished before current show starts
        # Since end times are inclusive, we use <= instead of <
        while occupied and occupied[0][0] < start:
            freed_end_time, freed_stage = heapq.heappop(occupied)
            heapq.heappush(free_stage_ids, freed_stage)

        # Assign to an available stage or create a new one
        if free_stage_ids:
            stage = heapq.heappop(free_stage_ids)
        else:
            stage = next_stage_id
            next_stage_id += 1

        # Record the assignment
        assignments[name] = stage
        stage_timelines[stage].append((name, start, end))
        
        # Mark this stage as occupied until the show ends
        heapq.heappush(occupied, (end, stage))

    num_stages = next_stage_id - 1
    return assignments, stage_timelines, num_stages


def print_schedule(assignments: Dict[str, int], 
                  stage_timelines: Dict[int, List[Tuple[str, int, int]]], 
                  num_stages: int, 
                  original_order: Optional[List[Tuple[str, int, int]]] = None) -> None:
    """
    Prints the scheduling results in a formatted way.
    
    Args:
        assignments: Dict mapping show names to stage numbers
        stage_timelines: Dict mapping stage numbers to lists of shows
        num_stages: Total number of stages required
        original_order: Optional list of shows in original input order
    """
    print(f"Total stages required: {num_stages}")
    
    if num_stages == 0:
        print("No shows to schedule.")
        return
        
    print()
    
    if original_order:
        print("Assignments in input order:")
        for name, start, end in original_order:
            stage = assignments[name]
            print(f"  {name}: {start} - {end}  --> Stage {stage}")
        print()
    
    print("Per-stage timelines:")
    for stage in sorted(stage_timelines.keys()):
        print(f"Stage {stage}:")
        # Sort shows on each stage by start time
        for name, start, end in sorted(stage_timelines[stage], key=lambda t: t[1]):
            print(f"  {name}: {start} - {end}")
        print()


def validate_schedule(assignments: Dict[str, int], 
                     shows: List[Tuple[str, int, int]]) -> bool:
    """
    Validates that the schedule has no overlapping shows on the same stage.
    
    Args:
        assignments: Dict mapping show names to stage numbers
        shows: List of (show_name, start_time, end_time) tuples
        
    Returns:
        True if schedule is valid, False otherwise
    """
    # Group shows by stage
    stage_shows = defaultdict(list)
    for name, start, end in shows:
        stage = assignments[name]
        stage_shows[stage].append((name, start, end))
    
    # Check each stage for overlaps
    for stage, stage_show_list in stage_shows.items():
        stage_show_list.sort(key=lambda x: x[1])  # Sort by start time
        
        for i in range(len(stage_show_list) - 1):
            current_show = stage_show_list[i]
            next_show = stage_show_list[i + 1]
            
            # Check if current show's end time overlaps with next show's start
            # Since end times are inclusive, we need current_end < next_start
            if current_show[2] >= next_show[1]:
                print(f"ERROR: Overlap detected on Stage {stage}:")
                print(f"  {current_show[0]} ({current_show[1]}-{current_show[2]}) overlaps with")
                print(f"  {next_show[0]} ({next_show[1]}-{next_show[2]})")
                return False
    
    return True


def main(argv: List[str]) -> None:
    """Main function to run the festival schedule generator."""
    try:
        # Read input
        if len(argv) > 1:
            filepath = argv[1]
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except FileNotFoundError:
                print(f"Error: File '{filepath}' not found.", file=sys.stderr)
                sys.exit(1)
            except IOError as e:
                print(f"Error reading file '{filepath}': {e}", file=sys.stderr)
                sys.exit(1)
        else:
            # Read from stdin
            try:
                content = sys.stdin.read().strip()
                lines = content.splitlines() if content else []
            except KeyboardInterrupt:
                print("\nOperation cancelled by user.", file=sys.stderr)
                sys.exit(1)

        # Parse shows
        shows = parse_lines(lines)
        
        if not shows:
            print("No shows found in input.")
            return
        
        # Generate schedule
        assignments, stage_timelines, num_stages = assign_stages(shows)
        
        # Validate the schedule (optional check)
        if not validate_schedule(assignments, shows):
            print("ERROR: Generated schedule is invalid!", file=sys.stderr)
            sys.exit(1)
        
        # Print results
        print_schedule(assignments, stage_timelines, num_stages, original_order=shows)
        
    except ValueError as e:
        print(f"Input error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main(sys.argv)
