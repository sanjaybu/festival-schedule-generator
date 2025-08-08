# Festival Schedule Generator

A Python-based solution for the **Demcon "Festival Schedule Generator" challenge** that automatically assigns shows to the minimum number of stages required, ensuring no overlapping shows occur on the same stage.

## Overview

This tool reads a list of shows (each with a name, start time, and end time) and uses an efficient greedy scheduling algorithm to determine the optimal stage allocation. The goal is to minimize the total number of stages while ensuring no time conflicts.

**Challenge Source:** [Demcon Careers - Festival Schedule Generator](https://careersatdemcon.com/decode-demcon/challenge-festival-schedule-generator)

## Features

- **Optimal Stage Assignment:** Uses a greedy algorithm with min-heap for efficient O(n log n) scheduling
- **Flexible Input Options:** Accepts input from files or standard input (stdin)
- **Inclusive End Times:** Properly handles back-to-back shows (end time is inclusive)
- **Comprehensive Output:** Shows total stages needed, assignments in input order, and detailed per-stage timelines
- **Input Validation:** Robust error handling for malformed input
- **Clean Architecture:** Modular, well-documented code ready for extensions

## Quick Start

### Prerequisites
- Python 3.8 or higher

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/festival-schedule-generator.git
   cd festival-schedule-generator
   ```

2. **Create input file:**
   ```bash
   # Create input.txt with your show schedule
   echo "ShowA 1 3
   ShowB 2 5
   ShowC 4 6
   ShowD 5 7" > input.txt
   ```

3. **Run the program:**
   ```bash
   python festival_schedule_generator.py input.txt
   ```

## Usage

### Input Format
Each line represents a show in the format:
```
<ShowName> <StartTime> <EndTime>
```

- **ShowName:** String identifier (no spaces)
- **StartTime/EndTime:** Integers representing time units
- **Important:** End times are **inclusive** (show ending at time 5 conflicts with show starting at time 5)

### Example Input (`input.txt`)
```
ShowA 1 3
ShowB 2 5
ShowC 4 6
ShowD 5 7
```

### Running Options

**From file:**
```bash
python festival_schedule_generator.py input.txt
```

**From standard input:**
```bash
cat input.txt | python festival_schedule_generator.py
# or
python festival_schedule_generator.py < input.txt
```

**Interactive input:**
```bash
python festival_schedule_generator.py
# Then type shows line by line, press Ctrl+D (Unix) or Ctrl+Z (Windows) when done
```

### Example Output
```
Total stages required: 3

Assignments in input order:
  ShowA: 1 - 3  --> Stage 1
  ShowB: 2 - 5  --> Stage 2
  ShowC: 4 - 6  --> Stage 1
  ShowD: 5 - 7  --> Stage 3

Per-stage timelines:
Stage 1:
  ShowA: 1 - 3
  ShowC: 4 - 6

Stage 2:
  ShowB: 2 - 5

Stage 3:
  ShowD: 5 - 7
```

## Algorithm Explanation

The solution uses a **greedy scheduling algorithm** with min-heap optimization:

### Step-by-Step Process:

1. **Parse & Validate:** Convert input lines to `(name, start, end)` tuples with validation
2. **Sort Shows:** Order by start time (then end time for ties)
3. **Track Stages:** Use two heaps:
   - `occupied`: Min-heap tracking when stages become free (by end time)
   - `free_stage_ids`: Available stage IDs for reuse
4. **Assign Shows:** For each show:
   - Free stages that ended before current show's start
   - Assign to earliest free stage or create new one
   - Update heaps with new assignment

### Time Complexity: O(n log n)
- Sorting: O(n log n)
- Heap operations: O(n log n)
- Overall: O(n log n) where n is the number of shows

### Space Complexity: O(n)

## 📁 Project Structure

```
festival-schedule-generator/
├── festival_schedule_generator.py  # Main application
├── input.txt                      # Example input file
├── README.md                      # This documentation
└── requirements.txt               # Dependencies (empty - uses stdlib only)
```

## Testing Examples

### Example 1: Basic Overlap
**Input:**
```
ShowA 1 3
ShowB 2 4
ShowC 3 5
```
**Output:** 2 stages (ShowA and ShowC share stage 1, ShowB gets stage 2)

### Example 2: No Overlaps
**Input:**
```
ShowA 1 2
ShowB 3 4
ShowC 5 6
```
**Output:** 1 stage (all shows sequential)

### Example 3: Complex Schedule
**Input:**
```
Show1 1 5
Show2 2 3
Show3 4 6
Show4 6 8
Show5 7 9
```
**Output:** 3 stages needed

## Advanced Usage

### Custom Input Validation
The program handles various edge cases:
- Empty lines and comments (lines starting with `#`)
- Invalid time formats
- End time before start time
- Missing fields

### Error Handling
```python
# Example error messages:
# "Line 2: expected 3 tokens, got: 'ShowA 1'"
# "Line 3: start/end must be integers: 'ShowB start end'"
# "Line 4: end < start: 'ShowC 5 2'"
```

## Contributing
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Commit: `git commit -am 'Add feature'`
5. Push: `git push origin feature-name`
6. Submit a pull request


## Challenge Details

This solution addresses the Demcon coding challenge requirements:
- Minimal number of stages
- No overlapping shows on same stage
- Handles inclusive end times
- Clear, readable output
- Efficient algorithm implementation

## Support

If you encounter any issues or have questions:
1. Check the example inputs and outputs above
2. Ensure your input follows the correct format
3. Verify Python 3.8+ is installed
4. Open an issue on GitHub for bugs or feature requests

---

**Created for the Demcon Festival Schedule Generator Challenge**
