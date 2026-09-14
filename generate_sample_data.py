#!/usr/bin/env python3
"""
generate_sample_data.py
---------------------------------------------------------------------------
Pre-processing / test-data generation script.

This is a SECOND, separate script (in addition to the main
payroll_processor.py program) that creates a randomised timesheet input
file. It is useful for generating fresh test data to demonstrate that the
main program works correctly for different inputs, and satisfies the
optional brief feature: "Use of multiple scripts that pre- or post-process
the data files".

Usage:
    python3 generate_sample_data.py [number_of_employees] [output_file]

Example:
    python3 generate_sample_data.py 10 data/timesheet_random.txt
---------------------------------------------------------------------------
"""

import sys
import random

# A small pool of sample names used to build believable-looking test data
FIRST_NAMES = ["Amelia", "Noah", "Rahima", "Liam", "Sophia", "Omar",
               "Grace", "Ethan", "Priya", "Jack"]
LAST_NAMES = ["Turner", "Ahmed", "Begum", "Smith", "Chowdhury",
              "Walker", "Rahman", "Hughes", "Patel", "Brooks"]


def generate_employee_line(employee_number):
    """
    Build one comma-separated timesheet line for a single fictitious
    employee, with a random hourly rate, tax rate and five days of
    random working hours (occasionally including overtime so the main
    program's overtime logic is exercised by the sample data).

    Parameters
    ----------
    employee_number : int
        Used to build a simple, unique employee ID (e.g. E001, E002...).

    Returns
    -------
    str
        A single formatted timesheet line, without a trailing newline.
    """
    employee_id = f"E{employee_number:03d}"
    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    hourly_rate = round(random.uniform(11.50, 22.00), 2)
    tax_rate = round(random.uniform(0.15, 0.25), 2)
    # Most days are a normal 6-9 hour shift; occasionally push hours up
    # so that some employees trigger the overtime calculation.
    daily_hours = [round(random.uniform(6.0, 9.5), 1) for _ in range(5)]

    fields = [employee_id, name, f"{hourly_rate}", f"{tax_rate}"] + \
             [f"{h}" for h in daily_hours]
    return ",".join(fields)


def main():
    """Entry point: parse arguments and write the generated file."""
    employee_count = int(sys.argv[1]) if len(sys.argv) >= 2 else 5
    output_file = sys.argv[2] if len(sys.argv) >= 3 else "data/timesheet_random.txt"

    with open(output_file, "w") as file:
        file.write("# Auto-generated sample timesheet data\n")
        file.write("# EmployeeID,Name,HourlyRate,TaxRate,Mon,Tue,Wed,Thu,Fri\n")
        for i in range(1, employee_count + 1):
            file.write(generate_employee_line(i) + "\n")

    print(f"Generated {employee_count} sample employee record(s) -> {output_file}")


if __name__ == "__main__":
    main()
