# Employee Data Analyzer

A Python 3 command-line tool that cleans employee data from a CSV file and produces simple insights: headcount, average and highest salary, total payroll, department-wise averages, and employees above a salary limit, along with a bar chart.

**Concepts used:** Pandas, Filtering, Grouping, Aggregation

## Project Summary

HR teams often receive employee data that is messy: duplicate rows, blank salaries, inconsistent spacing. This project loads such a file with Pandas, cleans it, and answers common questions through a small menu.

**Cleaning rules**
1. Duplicate employees (same `Emp_ID`) are removed, keeping the first occurrence.
2. Missing salaries are filled with the **mean of the valid salaries** (calculated after duplicates are removed).
3. Salary and Experience are converted to numbers; extra whitespace is trimmed.

**Insights**
| Menu option | What it does |
|---|---|
| 1. Summary | Employee count, average salary, highest paid employee, total payroll (plus a cleaning report if duplicates or blanks were found) |
| 2. Department-wise + filter | Employee count and average salary per department, list of employees above a salary limit, and a bar chart "Department-wise Average Salary" |
| 3. Exit | Quit the program |

## Requirements

- Python 3.8+
- `pandas`
- `matplotlib`

```bash
pip install pandas matplotlib
```

## CSV Format

No header row; columns in this order (dummy data only):

```
Emp_ID,Name,Department,Salary,Experience
E1,Aman,IT,50000,3
E2,Riya,HR,40000,2
E3,Karan,IT,70000,5
```

## How to Run

Interactive menu (reads `employees.csv` by default):

```bash
python3 analyzer.py
python3 analyzer.py path/to/data.csv
```

Run a single option directly:

```bash
python3 analyzer.py employees.csv -o 1                # Summary
python3 analyzer.py employees.csv -o 2 -l 45000       # Department-wise + salary filter
```

The chart opens in a window when a display is available and is always saved as `department_avg_salary.png`.

## Project Files

| File | Purpose |
|---|---|
| `analyzer.py` | The analyzer program |
| `employees.csv` | Sample data (Test Cases 1 and 4) |
| `employees_case2.csv` | Single-row data (Test Case 2) |
| `employees_case3.csv` | Data with a duplicate and a missing salary (Test Case 3) |
| `screenshots/` | Output screenshots for each test case |

## Test Cases

### Test Case 1: Normal Input
Three employees, menu option 1 (Summary).

**Expected:** `Employees: 3 │ Average salary: 53333.33`, `Highest paid: Karan (70000)`, `Total payroll: 160000`

![Test Case 1](screenshots/test_case_1.png)

### Test Case 2: Boundary / Minimum Input
A single row, menu option 1 (Summary).

**Expected:** `Employees: 1 │ Average salary: 50000.00`, `Highest paid: Aman (50000)`

![Test Case 2](screenshots/test_case_2.png)

### Test Case 3: Invalid Input
Test Case 1 data plus a duplicate row (`E1`) and a row with a missing salary (`E4`).

**Expected:** `Duplicates removed: 1`, `Missing Salary filled with mean: 53333.33`, `Cleaned rows: 4`

![Test Case 3](screenshots/test_case_3.png)

### Test Case 4: Different Valid Scenario
Same data as Test Case 1, menu option 2 with a limit of 45000.

**Expected:** IT: 2 employees │ Avg salary 60000.00, HR: 1 employee │ Avg salary 40000.00, Above 45000: Aman (50000) │ Karan (70000), and the bar chart.

![Test Case 4](screenshots/test_case_4.png)

![Department-wise Average Salary chart](screenshots/test_case_4_chart.png)

## Error Handling

The program exits with a clear message if the file is missing, empty, contains no records, or has no valid salaries. Invalid menu choices are reported and the menu is shown again.
