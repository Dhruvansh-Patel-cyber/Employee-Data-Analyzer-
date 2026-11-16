"""Employee Data Analyzer

Cleans an employee CSV and reports insights using pandas.
CSV columns: Emp_ID, Name, Department, Salary, Experience

Usage:
    python3 analyzer.py                      # interactive menu, uses employees.csv
    python3 analyzer.py data.csv             # interactive menu, custom file
    python3 analyzer.py data.csv -o 1        # run one menu option and exit
    python3 analyzer.py data.csv -o 2 -l 45000
"""

import argparse
import sys

import matplotlib
import pandas as pd

COLUMNS = ["Emp_ID", "Name", "Department", "Salary", "Experience"]
DEFAULT_LIMIT = 45000
CHART_FILE = "department_avg_salary.png"


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def fmt_money(value):
    """Whole numbers print without decimals (70000); others with 2 (53333.33)."""
    value = float(value)
    return str(int(value)) if value.is_integer() else f"{value:.2f}"


def plural(n, word):
    return f"{n} {word}" if n == 1 else f"{n} {word}s"


# --------------------------------------------------------------------------
# Loading and cleaning
# --------------------------------------------------------------------------
def load_and_clean(path):
    """Read the CSV and clean it.

    Steps: drop duplicate Emp_IDs, coerce Salary/Experience to numbers,
    fill missing salaries with the mean of the valid (non-missing) salaries.

    Returns (clean_df, report) where report holds counts for display.
    """
    df = pd.read_csv(path, header=None, names=COLUMNS, skipinitialspace=True)

    # Tolerate a header row if the file has one.
    if not df.empty and str(df.iloc[0]["Emp_ID"]).strip().lower() == "emp_id":
        df = df.iloc[1:]

    df = df.dropna(how="all").copy()
    for col in ("Emp_ID", "Name", "Department"):
        df[col] = df[col].astype("string").str.strip()

    before = len(df)
    df = df.drop_duplicates(subset="Emp_ID", keep="first")
    duplicates_removed = before - len(df)

    df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce")
    df["Experience"] = pd.to_numeric(df["Experience"], errors="coerce")

    missing = int(df["Salary"].isna().sum())
    mean_salary = df["Salary"].mean()  # NaN-skipping: mean of valid salaries
    if missing and pd.notna(mean_salary):
        df["Salary"] = df["Salary"].fillna(mean_salary)

    df = df.reset_index(drop=True)
    report = {
        "duplicates_removed": duplicates_removed,
        "missing_filled": missing if pd.notna(mean_salary) else 0,
        "mean_used": mean_salary,
        "cleaned_rows": len(df),
    }
    return df, report


# --------------------------------------------------------------------------
# Insights
# --------------------------------------------------------------------------
def print_cleaning_report(report):
    if report["duplicates_removed"]:
        print(f"Duplicates removed: {report['duplicates_removed']}")
    if report["missing_filled"]:
        print(f"Missing Salary filled with mean: {report['mean_used']:.2f}")
    if report["duplicates_removed"] or report["missing_filled"]:
        print(f"Cleaned rows: {report['cleaned_rows']}")


def summary(df, report):
    print_cleaning_report(report)
    top = df.loc[df["Salary"].idxmax()]
    print(f"Employees: {len(df)} │ Average salary: {df['Salary'].mean():.2f}")
    print(f"Highest paid: {top['Name']} ({fmt_money(top['Salary'])})")
    print(f"Total payroll: {fmt_money(df['Salary'].sum())}")


def department_report(df, report, limit):
    print_cleaning_report(report)

    # sort=False keeps departments in order of first appearance
    grouped = df.groupby("Department", sort=False)["Salary"].agg(["count", "mean"])
    for dept, row in grouped.iterrows():
        print(f"{dept}: {plural(int(row['count']), 'employee')} │ "
              f"Avg salary: {row['mean']:.2f}")

    above = df[df["Salary"] > limit]
    if above.empty:
        print(f"Above {fmt_money(limit)}: none")
    else:
        names = " │ ".join(
            f"{r['Name']} ({fmt_money(r['Salary'])})" for _, r in above.iterrows()
        )
        print(f"Above {fmt_money(limit)}: {names}")

    draw_chart(grouped["mean"])


def draw_chart(avg_by_dept):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(avg_by_dept.index, avg_by_dept.values, color="#3b6fb6")
    ax.bar_label(bars, labels=[f"{v:,.0f}" for v in avg_by_dept.values], padding=3)
    ax.set_title("Department-wise Average Salary")
    ax.set_xlabel("Department")
    ax.set_ylabel("Average Salary")
    ax.set_ylim(0, avg_by_dept.max() * 1.15)
    fig.tight_layout()
    fig.savefig(CHART_FILE, dpi=150)
    print(f"Bar chart 'Department-wise Average Salary' displayed (saved as {CHART_FILE})")

    # Only open a window when a GUI backend is active.
    if matplotlib.get_backend().lower() not in ("agg", "pdf", "svg", "ps", "cairo", "template"):
        plt.show()
    plt.close(fig)


# --------------------------------------------------------------------------
# Menu / CLI
# --------------------------------------------------------------------------
def ask_limit():
    raw = input(f"Salary limit [{DEFAULT_LIMIT}]: ").strip()
    if not raw:
        return DEFAULT_LIMIT
    try:
        return float(raw)
    except ValueError:
        print(f"Invalid number, using {DEFAULT_LIMIT}.")
        return DEFAULT_LIMIT


def run_option(choice, df, report, limit=None):
    if choice == "1":
        summary(df, report)
    elif choice == "2":
        department_report(df, report, ask_limit() if limit is None else limit)
    else:
        print("Invalid option. Choose 1, 2 or 3.")


def main():
    parser = argparse.ArgumentParser(description="Employee Data Analyzer")
    parser.add_argument("csv", nargs="?", default="employees.csv")
    parser.add_argument("-o", "--option", choices=["1", "2"], help="run one option and exit")
    parser.add_argument("-l", "--limit", type=float, help="salary limit for option 2")
    args = parser.parse_args()

    try:
        df, report = load_and_clean(args.csv)
    except FileNotFoundError:
        sys.exit(f"Error: file '{args.csv}' not found.")
    except pd.errors.EmptyDataError:
        sys.exit(f"Error: '{args.csv}' is empty.")

    if df.empty:
        sys.exit("Error: no employee records found.")
    if df["Salary"].isna().all():
        sys.exit("Error: no valid salaries in the file.")

    if args.option:
        run_option(args.option, df, report, args.limit)
        return

    while True:
        print("\n=== Employee Data Analyzer ===")
        print("1. Summary")
        print("2. Department-wise and filter above salary limit")
        print("3. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "3":
            print("Goodbye!")
            break
        print()
        run_option(choice, df, report)


if __name__ == "__main__":
    main()