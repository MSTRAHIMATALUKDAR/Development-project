@echo off
REM ---------------------------------------------------------------------
REM run_payroll.bat
REM ---------------------------------------------------------------------
REM Script file that executes the Data Processing program from a
REM Command Line Interface (CLI) on Windows.
REM
REM This is provided alongside run_payroll.sh (bash) so the project can
REM be run from an accepted CLI on more than one platform - an example
REM of the optional "Use of multiple scripting languages for use on
REM different platforms" feature from the brief.
REM
REM Usage:
REM   run_payroll.bat                     (uses the default sample file)
REM   run_payroll.bat data\myfile.txt     (uses a specific input file)
REM ---------------------------------------------------------------------

REM %1 is the first command-line argument passed to this script.
REM If it was not supplied, fall back to the sample timesheet file.
SET INPUT_FILE=%1
IF "%INPUT_FILE%"=="" SET INPUT_FILE=data\timesheet.txt
SET OUTPUT_FOLDER=output

echo ============================================================
echo  Running Payroll Data Processing Program
echo  Input file : %INPUT_FILE%
echo ============================================================

REM Check the input file exists before running the program
IF NOT EXIST "%INPUT_FILE%" (
    echo ERROR: Input file "%INPUT_FILE%" was not found.
    exit /b 1
)

REM Execute the main Python data processing program, passing the input
REM file and output folder in as command-line arguments.
python payroll_processor.py "%INPUT_FILE%" "%OUTPUT_FOLDER%"

echo ============================================================
echo  Done. See the "%OUTPUT_FOLDER%" folder for paycheck.txt and report.txt
echo ============================================================
