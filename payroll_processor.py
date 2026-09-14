#!/usr/bin/env python3
"""
payroll_processor.py
---------------------------------------------------------------------------
Employee Payroll Data Processing Program
---------------------------------------------------------------------------
Module      : CPUF001 - Software Foundation
Assignment  : Development Project (Assessment 1)

Purpose
-------
This program reads employee timesheet data from an input CSV-style text
file (supplied as a command-line argument), performs payroll calculations
(regular pay, overtime pay, tax deduction and net take-home pay) for each
employee, and writes the results to:

    1. An output "paycheck" file containing an itemised breakdown for
       every employee.
    2. A summary "report" file that gives an overview of the whole
       payroll run (totals, averages, and any errors encountered).

The program builds on the simple single-employee example provided in the
module materials (week 4: payroll.py, timesheet.txt, paycheck.txt) and
extends it to process multiple employees, multiple data fields per
employee, and to include validation and error handling so that a single
bad record does not stop the whole payroll run.

Usage (from the command line)
------------------------------
    python3 payroll_processor.py <input_timesheet_file> [output_folder]

Example:
    python3 payroll_processor.py data/timesheet.txt output

Input file format
------------------
Each line in the input file represents ONE employee, with the following
comma-separated fields (9 values per line - well above the brief's
minimum requirement of 3 data values read from the file):

    EmployeeID,Name,HourlyRate,TaxRate,MonHours,TueHours,WedHours,
    ThuHours,FriHours

Example line:
    E001,Amelia Turner,14.50,0.20,8,7.5,8,8,6

Lines starting with '#' are treated as comments and skipped.
---------------------------------------------------------------------------
"""

import sys
import os
from datetime import datetime

# ---------------------------------------------------------------------------
# Configuration constants
# ---------------------------------------------------------------------------
# Grouping these "magic numbers" as named constants (rather than scattering
# literal values through the code) makes the rules of the business easy to
# find and change in one place - an example of writing maintainable code.
OVERTIME_THRESHOLD_HOURS = 40.0   # hours per week before overtime applies
OVERTIME_MULTIPLIER = 1.5         # overtime is paid at 1.5x the normal rate
EXPECTED_FIELD_COUNT = 9          # EmployeeID, Name, Rate, Tax, 5 day hours


# ---------------------------------------------------------------------------
# Data structure
# ---------------------------------------------------------------------------
class Employee:
    """
    Represents a single employee's timesheet record and the payroll
    results calculated for them.

    Using a class here (rather than passing several loose variables or a
    plain tuple around) keeps each employee's data and results bundled
    together, which makes the rest of the program easier to read and
    reduces the chance of mixing up one employee's figures with another's.
    """

    def __init__(self, employee_id, name, hourly_rate, tax_rate, daily_hours):
        self.employee_id = employee_id
        self.name = name
        self.hourly_rate = hourly_rate
        self.tax_rate = tax_rate
        self.daily_hours = daily_hours          # list of 5 floats
        self.total_hours = 0.0
        self.regular_hours = 0.0
        self.overtime_hours = 0.0
        self.gross_pay = 0.0
        self.tax_amount = 0.0
        self.net_pay = 0.0


# ---------------------------------------------------------------------------
# Function: read_timesheet_file
# ---------------------------------------------------------------------------
def read_timesheet_file(file_name):
    """
    Read and parse the timesheet input file.

    Each valid line is converted into an Employee object. Lines that are
    blank or start with '#' are skipped. Lines that are malformed
    (wrong number of fields, or fields that cannot be converted to the
    expected numeric type) are NOT allowed to crash the whole program;
    instead they are recorded as errors and processing continues with
    the remaining lines. This satisfies the "error checking and
    handling, especially with files" requirement.

    Parameters
    ----------
    file_name : str
        Path to the input timesheet file.

    Returns
    -------
    tuple (list[Employee], list[str])
        A list of successfully parsed Employee objects, and a list of
        human-readable error messages for any lines that failed to parse.

    Raises
    ------
    FileNotFoundError
        Propagated to the caller if the file itself cannot be opened, so
        that the top-level program can report a clear message and exit
        cleanly rather than printing a raw Python traceback.
    """
    employees = []
    errors = []

    with open(file_name, "r") as file:            # 'with' guarantees the file is closed
        for line_number, raw_line in enumerate(file.readlines(), start=1):
            line = raw_line.strip()

            # Skip blank lines and comment lines
            if not line or line.startswith("#"):
                continue

            fields = [f.strip() for f in line.split(",")]

            if len(fields) != EXPECTED_FIELD_COUNT:
                errors.append(
                    f"Line {line_number}: expected {EXPECTED_FIELD_COUNT} "
                    f"fields but found {len(fields)} -> '{line}'"
                )
                continue

            try:
                employee_id = fields[0]
                name = fields[1]
                hourly_rate = float(fields[2])
                tax_rate = float(fields[3])
                daily_hours = [float(h) for h in fields[4:9]]

                # Basic sanity / validation checks (defensive programming)
                if hourly_rate <= 0:
                    raise ValueError("hourly rate must be greater than zero")
                if not (0 <= tax_rate < 1):
                    raise ValueError("tax rate must be between 0 and 1")
                if any(h < 0 or h > 24 for h in daily_hours):
                    raise ValueError("daily hours must be between 0 and 24")

                employees.append(
                    Employee(employee_id, name, hourly_rate, tax_rate, daily_hours)
                )

            except ValueError as err:
                errors.append(f"Line {line_number}: invalid data ({err}) -> '{line}'")

    return employees, errors


# ---------------------------------------------------------------------------
# Function: calculate_pay
# ---------------------------------------------------------------------------
def calculate_pay(employee):
    """
    Perform the payroll calculations for one employee and store the
    results directly on the Employee object.

    Calculations performed (this satisfies the "at least 2 calculations"
    requirement - four related calculations are performed here):
        1. Total hours worked, split into regular hours and overtime hours
        2. Gross pay (regular pay + overtime pay at 1.5x rate)
        3. Tax deducted (gross pay * employee tax rate)
        4. Net (take-home) pay (gross pay - tax)

    Parameters
    ----------
    employee : Employee
        The employee record to calculate pay for. Modified in place.
    """
    employee.total_hours = sum(employee.daily_hours)

    if employee.total_hours > OVERTIME_THRESHOLD_HOURS:
        employee.regular_hours = OVERTIME_THRESHOLD_HOURS
        employee.overtime_hours = employee.total_hours - OVERTIME_THRESHOLD_HOURS
    else:
        employee.regular_hours = employee.total_hours
        employee.overtime_hours = 0.0

    regular_pay = employee.regular_hours * employee.hourly_rate
    overtime_pay = employee.overtime_hours * employee.hourly_rate * OVERTIME_MULTIPLIER

    employee.gross_pay = regular_pay + overtime_pay
    employee.tax_amount = employee.gross_pay * employee.tax_rate
    employee.net_pay = employee.gross_pay - employee.tax_amount


# ---------------------------------------------------------------------------
# Function: write_paycheck_file
# ---------------------------------------------------------------------------
def write_paycheck_file(output_file_name, employees):
    """
    Write a formatted, itemised paycheck breakdown for every employee to
    the given output file.

    Parameters
    ----------
    output_file_name : str
        Path of the paycheck file to create/overwrite.
    employees : list[Employee]
        Employees to include in the file (in the order supplied).
    """
    with open(output_file_name, "w") as file:
        file.write("=" * 60 + "\n")
        file.write("EMPLOYEE PAYCHECK BREAKDOWN\n")
        file.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write("=" * 60 + "\n\n")

        for emp in employees:
            file.write(f"Employee ID   : {emp.employee_id}\n")
            file.write(f"Name          : {emp.name}\n")
            file.write(f"Hourly Rate   : £{emp.hourly_rate:.2f}\n")
            file.write(f"Total Hours   : {emp.total_hours:.2f}\n")
            file.write(f"Regular Hours : {emp.regular_hours:.2f}\n")
            file.write(f"Overtime Hours: {emp.overtime_hours:.2f}\n")
            file.write(f"Gross Pay     : £{emp.gross_pay:.2f}\n")
            file.write(f"Tax ({emp.tax_rate*100:.0f}%)     : £{emp.tax_amount:.2f}\n")
            file.write(f"Net Pay       : £{emp.net_pay:.2f}\n")
            file.write("-" * 60 + "\n")


# ---------------------------------------------------------------------------
# Function: write_summary_report
# ---------------------------------------------------------------------------
def write_summary_report(report_file_name, employees, errors, input_file_name):
    """
    Write a summary report of the whole payroll processing run.

    This is an additional feature beyond the brief's minimum requirements
    ("Output of report file that summarises processing activity") and
    gives a manager-level overview rather than per-employee detail.

    Parameters
    ----------
    report_file_name : str
        Path of the report file to create/overwrite.
    employees : list[Employee]
        Successfully processed employees.
    errors : list[str]
        Any error messages generated while reading/validating the input.
    input_file_name : str
        The original input file name, included for traceability.
    """
    with open(report_file_name, "w") as file:
        file.write("=" * 60 + "\n")
        file.write("PAYROLL PROCESSING SUMMARY REPORT\n")
        file.write(f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"Source    : {input_file_name}\n")
        file.write("=" * 60 + "\n\n")

        file.write(f"Employees successfully processed : {len(employees)}\n")
        file.write(f"Records skipped due to errors     : {len(errors)}\n\n")

        if employees:
            total_gross = sum(e.gross_pay for e in employees)
            total_tax = sum(e.tax_amount for e in employees)
            total_net = sum(e.net_pay for e in employees)
            average_net = total_net / len(employees)
            highest_paid = max(employees, key=lambda e: e.net_pay)
            lowest_paid = min(employees, key=lambda e: e.net_pay)

            file.write(f"Total gross pay (all employees)  : £{total_gross:.2f}\n")
            file.write(f"Total tax deducted                : £{total_tax:.2f}\n")
            file.write(f"Total net pay (all employees)     : £{total_net:.2f}\n")
            file.write(f"Average net pay per employee       : £{average_net:.2f}\n\n")
            file.write(f"Highest paid employee : {highest_paid.name} (£{highest_paid.net_pay:.2f})\n")
            file.write(f"Lowest paid employee  : {lowest_paid.name} (£{lowest_paid.net_pay:.2f})\n")
        else:
            file.write("No employee records were successfully processed.\n")

        if errors:
            file.write("\n" + "-" * 60 + "\n")
            file.write("ERRORS ENCOUNTERED\n")
            file.write("-" * 60 + "\n")
            for error in errors:
                file.write(f" - {error}\n")


# ---------------------------------------------------------------------------
# Function: main
# ---------------------------------------------------------------------------
def main():
    """
    Program entry point. Reads command-line arguments, orchestrates the
    read -> calculate -> write pipeline, and handles top-level errors so
    the user always sees a clear message instead of a raw traceback.
    """
    # --- Command line argument handling -----------------------------------
    if len(sys.argv) < 2:
        print("Usage: python3 payroll_processor.py <input_timesheet_file> [output_folder]")
        sys.exit(1)

    input_file_name = sys.argv[1]
    output_folder = sys.argv[2] if len(sys.argv) >= 3 else "output"

    # Make sure the output folder exists before we try to write into it
    os.makedirs(output_folder, exist_ok=True)

    paycheck_file = os.path.join(output_folder, "paycheck.txt")
    report_file = os.path.join(output_folder, "report.txt")

    # --- Read and validate input --------------------------------------
    try:
        employees, errors = read_timesheet_file(input_file_name)
    except FileNotFoundError:
        print(f"ERROR: Input file '{input_file_name}' was not found. "
              f"Please check the file path and try again.")
        sys.exit(1)
    except OSError as err:
        print(f"ERROR: Could not read '{input_file_name}': {err}")
        sys.exit(1)

    # --- Calculate pay for every valid employee -----------------------
    for employee in employees:
        calculate_pay(employee)

    # --- Write output files --------------------------------------------
    write_paycheck_file(paycheck_file, employees)
    write_summary_report(report_file, employees, errors, input_file_name)

    # --- Console feedback for the user ----------------------------------
    print(f"Processed {len(employees)} employee record(s) from '{input_file_name}'.")
    if errors:
        print(f"{len(errors)} record(s) were skipped due to errors "
              f"(see {report_file} for details).")
    print(f"Paycheck details written to : {paycheck_file}")
    print(f"Summary report written to   : {report_file}")


# Standard Python entry-point guard: code inside this block only runs
# when the file is executed directly (e.g. `python3 payroll_processor.py`),
# not when it is imported as a module by another script.
if __name__ == "__main__":
    main()
