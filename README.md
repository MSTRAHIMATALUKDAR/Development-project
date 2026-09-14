# Employee Payroll Data Processing Program

CPUF001 – Software Foundation | Assessment 1: Development Project

## What this program does

`payroll_processor.py` is a command-line Python program that reads employee
timesheet data from an input file, calculates each employee's regular pay,
overtime pay, tax deduction and net take-home pay, and writes the results to
an output paycheck file and a summary report file.

It builds on the single-employee example provided in the module materials
(`payroll.py`, `timesheet.txt`, `paycheck.txt`) and extends it to handle
multiple employees, more input fields per employee, and file/data error
handling.

## Project structure

```
payroll_processor.py         Main data processing program
generate_sample_data.py      Second script: generates randomised test data
run_payroll.sh               CLI script to run the program (Linux / macOS)
run_payroll.bat              CLI script to run the program (Windows)
data/
    timesheet.txt             Sample input file (5 employees, all valid)
    timesheet_with_errors.txt Sample input file used to demonstrate error handling
output/                      Paycheck + report generated from timesheet.txt
output_error_demo/           Paycheck + report generated from timesheet_with_errors.txt
```

## Requirements

* Python 3.6 or later (no third-party libraries required — standard
  library only).

## How to run it

### Linux / macOS

```bash
chmod +x run_payroll.sh
./run_payroll.sh data/timesheet.txt
```

### Windows

```bat
run_payroll.bat data\timesheet.txt
```

### Or run the Python program directly on any platform

```bash
python3 payroll_processor.py data/timesheet.txt output
```

Output files (`paycheck.txt` and `report.txt`) are written to the `output`
folder (or whichever folder you pass as the second argument).

## Input file format

Each line represents one employee as 9 comma-separated values:

```
EmployeeID,Name,HourlyRate,TaxRate,MonHours,TueHours,WedHours,ThuHours,FriHours
```

Example:

```
E001,Amelia Turner,14.50,0.20,8,7.5,8,8,6
```

Lines starting with `#` are treated as comments and ignored.

## Generating extra test data

```bash
python3 generate_sample_data.py 10 data/timesheet_random.txt
```

This creates a new randomised 10-employee timesheet file that can be fed
into `payroll_processor.py` in the same way as any other input file.

## Author

Rahima — CPUF001 Software Foundation, Development Project.
