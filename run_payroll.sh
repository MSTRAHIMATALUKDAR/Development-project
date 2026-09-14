#!/bin/bash
# ---------------------------------------------------------------------------
# run_payroll.sh
# ---------------------------------------------------------------------------
# Script file that executes the Data Processing program from a
# Command Line Interface (CLI) on Linux / macOS (bash).
#
# It demonstrates the "Script file" deliverable required by the brief:
#   - It runs from an accepted CLI (bash)
#   - It executes the Data Processing program (payroll_processor.py),
#     passing an available data file in as a command-line argument
#   - It includes comments that explain each step
#
# Usage:
#   ./run_payroll.sh                     (uses the default sample file)
#   ./run_payroll.sh data/myfile.txt     (uses a specific input file)
# ---------------------------------------------------------------------------

# Stop the script immediately if any command fails (basic error handling)
set -e

# If the user supplies an input file as the first argument, use it.
# Otherwise, fall back to the sample timesheet included with the project.
INPUT_FILE="${1:-data/timesheet.txt}"
OUTPUT_FOLDER="output"

echo "============================================================"
echo " Running Payroll Data Processing Program"
echo " Input file : $INPUT_FILE"
echo "============================================================"

# Check the input file exists before trying to run the program, so we
# can give the user a clear message instead of a Python traceback.
if [ ! -f "$INPUT_FILE" ]; then
    echo "ERROR: Input file '$INPUT_FILE' was not found."
    exit 1
fi

# Execute the main Python data processing program, passing the input
# file and output folder in as command-line arguments.
python3 payroll_processor.py "$INPUT_FILE" "$OUTPUT_FOLDER"

echo "============================================================"
echo " Done. See the '$OUTPUT_FOLDER' folder for paycheck.txt and report.txt"
echo "============================================================"
