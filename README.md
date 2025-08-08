# Festival Schedule Generator

## Overview

The **Festival Schedule Generator** is a Python tool designed to solve the Demcon challenge of scheduling multiple shows across stages with minimal overlap. The goal is to allocate shows to as few stages as possible, ensuring no two shows on the same stage overlap in time.

This project reads a list of shows (each with a name, start time, and end time) and outputs a schedule showing which stage each show should be assigned to, minimizing the total number of stages required.

---

## Features

- **Optimal stage assignment:** Uses a greedy scheduling algorithm with a min-heap to assign shows efficiently.
- **Flexible input:** Accepts input from a file or standard input.
- **Inclusive end times:** Treats end times as inclusive, ensuring proper handling of back-to-back shows.
- **Detailed output:** Prints total stages required, assignments in input order, and per-stage timelines.
- **Easy to extend:** Clean, modular code ready for enhancements or integration.

---

## How It Works (Logic Explained)

1. **Parsing Input:**  
   Reads each show line and extracts `(name, start, end)` tuples. Validates input format and values.

2. **Sorting Shows:**  
   Sorts the shows by start time (and end time to break ties) to process them chronologically.

3. **Stage Assignment Using Min-Heap:**  
   Maintains two heaps:  
   - **Occupied stages heap:** Keeps track of when a stage becomes free (based on end times).  
   - **Free stages heap:** Stores available stage IDs ready to be reassigned.

   For each show in sorted order:
   - Frees up all stages whose shows ended strictly before the current show's start time.
   - Assigns the current show to the earliest free stage if available, or creates a new stage.
   - Updates heaps accordingly.

4. **Result Compilation:**  
   Tracks assignments and timelines to print comprehensive results.

---

## Setup Instructions

### Prerequisites

- Python 3.8 or higher installed on your system.

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/<your-username>/festival-schedule-generator.git
   cd festival-schedule-generator
2. (Optional) Create and activate a virtual environment:
    ```bash   
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
3. No external packages required; all dependencies are in the standard library.
  

