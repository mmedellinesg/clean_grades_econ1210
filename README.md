# Canvas Gradebook Formatter
This script processes problem set grades from an Excel file and merges them with a Canvas gradebook CSV, ensuring proper formatting for uploading to Canvas.

## Features
✅ Reads Canvas gradebook CSV and extracts relevant student information

✅ Loads problem set grades from an Excel file (organized by sheet)

✅ Matches student names between both datasets

✅ Corrects grade formatting, including date-like grade errors

✅ Saves the cleaned grades as a CSV for direct upload to Canvas

## Installation

Clone this repository:
```bash
git clone https://github.com/mmedellinesg/clean_grades_econ1210.git
cd clean_grades_econ1210
```
Install required Python packages:
```bash
pip install pandas openpyxl
```

## Usage
Run the script from the command line:

```bash
python clean_pset_grades_export.py <canvas_gradebook.csv> <psets.xlsx> <pset_number>
```
Example:
```bash
python clean_pset_grades_export.py gradebook.csv psets.xlsx 1
```
This processes PSET 1, matches student names, cleans the grades, and saves the output as:
📄 `gradebook_grades_ps1.csv`

## Input File Requirements
1. Canvas Gradebook (.csv)
Exported from Canvas
Must contain columns:
Student (full name)
ID
SIS Login ID
Section
Problem Set X (one column per problem set)
2. Problem Set File (.xlsx)
Must contain sheets named "PSET 1", "PSET 2", etc.
Each sheet should have:
Student (full name, case-insensitive)
Grade (numeric score, with date-like errors handled)

## Output
A cleaned CSV file named:
```php-template
<section>_grades_ps<pset>.csv
```
Example output file:
```
section1_grades_ps1.csv
```

## How It Works
1. Extracts section name from the Canvas filename
2. Loads Canvas gradebook and standardizes student names
3. Reads the correct PSET sheet from the Excel file
4. Fixes grade formatting, replacing date-like errors
5. Merges data, filling missing grades with existing values
6. Saves the final CSV
