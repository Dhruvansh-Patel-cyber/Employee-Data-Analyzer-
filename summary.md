# Employee Data Analyzer: Project Summary

## 1. Overview

The Employee Data Analyzer is a Python 3 program that reads employee records from a CSV file, cleans the data, and reports useful insights. It uses **Pandas** for loading, cleaning, filtering, grouping and aggregation, and **Matplotlib** for the bar chart.

**CSV columns:** `Emp_ID, Name, Department, Salary, Experience` (dummy data only)

**Features**
- Removes duplicate employees (same `Emp_ID`).
- Fills missing salaries with the mean of the valid salaries.
- Summary: number of employees, average salary, highest paid employee, total payroll.
- Department-wise employee count and average salary.
- Lists employees earning above a salary limit.
- Bar chart titled "Department-wise Average Salary".

## 2. How It Was Executed

### Step 1: Setup
Python 3 with `pandas` and `matplotlib` installed. The project folder holds `analyzer.py` and the sample CSV files.

```bash
pip install pandas matplotlib
```

### Step 2: Choosing the input file
The file is chosen from the command line. If no filename is given, the program uses `employees.csv`.

```bash
python analyzer.py                      # uses employees.csv
python analyzer.py employees_case2.csv  # uses the named file
```

### Step 3: Loading and cleaning the data (`load_and_clean`)
1. `pd.read_csv` reads the file with the five column names assigned (the CSV has no header row).
2. Extra spaces are trimmed from text columns.
3. `drop_duplicates(subset="Emp_ID")` removes repeated employees, keeping the first.
4. Salary and Experience are converted to numbers with `pd.to_numeric`.
5. Blank salaries are filled with the mean of the valid salaries.
6. The counts (duplicates removed, salaries filled, cleaned rows) are kept for display.

### Step 4: Menu and analysis
| Option | Action | Pandas concept |
|---|---|---|
| 1. Summary | Count, mean, max and sum of salaries | Aggregation |
| 2. Department-wise | `groupby("Department")` with count and mean; `df[df["Salary"] > limit]` for the filter; bar chart | Grouping, Filtering |
| 3. Exit | Ends the program | - |

A single option can also be run without the menu:

```bash
python analyzer.py employees.csv -o 1
python analyzer.py employees.csv -o 2 -l 45000
```

### Step 5: Testing
Four test cases were run and compared with the expected output.

| Test case | Input | Option | Result |
|---|---|---|---|
| 1. Normal | 3 employees | 1 | 3 employees, average 53333.33, Karan highest (70000), payroll 160000 |
| 2. Boundary | 1 employee | 1 | 1 employee, average 50000.00, Aman highest (50000) |
| 3. Invalid | Case 1 + duplicate + missing salary | 1 | 1 duplicate removed, salary filled with 53333.33, 4 cleaned rows |
| 4. Different valid | Case 1 data | 2 (limit 45000) | IT 2 / 60000.00, HR 1 / 40000.00, Aman and Karan above 45000, bar chart shown |

Screenshots of each run are in the `screenshots/` folder.

## 3. Difficulties Faced and How They Were Solved

| # | Difficulty | Solution |
|---|---|---|
| 1 | **The CSV has no header row**, so Pandas treated the first employee as column names and lost a record. | Read the file with `header=None` and supplied the column names manually. A header line is skipped if one is present. |
| 2 | **Duplicates affect the mean.** If the duplicate row is counted, the mean used to fill missing salaries changes. | Duplicates are removed first, then the mean is calculated. This gives the expected 53333.33 in Test Case 3. |
| 3 | **Which mean to use.** The missing salary must be filled with the mean of the *valid* salaries only, not including the blank. | `Series.mean()` skips blank values automatically, so the fill value is calculated before the blanks are filled. |
| 4 | **Number formatting.** The expected output shows `70000` for a salary but `53333.33` for an average. | A small helper prints whole numbers without decimals and other numbers with two decimals; averages use `:.2f`. |
| 5 | **Singular and plural wording.** The output needs "1 employee" and "2 employees". | A `plural()` helper chooses the correct word. |
| 6 | **Department order.** `groupby` sorts alphabetically by default, which put HR before IT and did not match the expected output. | Used `groupby(..., sort=False)` to keep the order in which departments first appear. |
| 7 | **Showing the chart without a screen.** The chart window cannot open on a machine with no display. | The chart is always saved as `department_avg_salary.png`, and a window is opened only when a display is available. |
| 8 | **Single-row and bad input.** One row, an empty file, a missing file or all-blank salaries could crash the program. | The program works with one row and shows a clear error message for a missing, empty or unusable file. |
| 9 | **Selecting the CSV file.** It was unclear how the program decided which file to read. | Used `argparse` with an optional filename that defaults to `employees.csv`. |

## 4. Conclusion

The program cleans the employee data and produces the summary, department-wise averages, salary filter and bar chart. It produces the expected output for all four test cases, including the boundary case (one row) and the invalid case (duplicate and missing salary).

**Possible improvements:** ask for the filename inside the program, save the cleaned data to a new CSV file, and add more filters (for example by experience).
