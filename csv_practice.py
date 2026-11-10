# ISM2411 Lab 12 — Read a Sales CSV, Write a Cleaned Report
# Author: Layton Niemier
# Run from the ism2411-lab12 folder:  python3 csv_practice.py
#
# REFLECTION
#
# 1. ETL in Python vs. Excel:
#    In Excel I could filter rows over $100 and add a Total column by hand, but I'd
#    have to repeat every click each time a new sales file arrived. Python does the
#    whole read-transform-write process in one run, works the same way every time,
#    and can handle files far too big for a spreadsheet or loop over hundreds of files.
#    Excel is still better for quickly eyeballing data, making a fast chart, or
#    sharing something a non-programmer can edit directly.
#
# 2. A business process that fits an append-mode log:
#    A wealth management firm could log each day's end-of-day portfolio value to a
#    text file: one line per day with the date and total assets. Append mode is the
#    right tool because every new entry must be added to the end without erasing
#    the history; write mode ("w") would wipe out all previous days each time it ran.

import csv
from datetime import datetime

SALES_FILE = "data/sales.csv"
CLEANED_FILE = "data/cleaned.csv"
LOG_FILE = "data/run_log.txt"

# ---------------------------------------------------------------------------
# EXERCISE 1 — Setup: confirm the file exists and opens without error
# ---------------------------------------------------------------------------
print("=== Exercise 1: Setup ===")
with open(SALES_FILE, "r") as f:
    print(f"Opened {SALES_FILE} successfully.")
print()

# ---------------------------------------------------------------------------
# EXERCISE 2 — Read and print raw rows (every value is a string)
# ---------------------------------------------------------------------------
print("=== Exercise 2: Raw rows ===")
with open(SALES_FILE, "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
print()

# ---------------------------------------------------------------------------
# EXERCISE 3 — Skip the header with next(reader)
# ---------------------------------------------------------------------------
print("=== Exercise 3: Header skipped ===")
with open(SALES_FILE, "r") as f:
    reader = csv.reader(f)
    header = next(reader)          # pulls off the first row
    print("Header:", header)
    for row in reader:             # loop now starts at the first data row
        print(row)
print()

# ---------------------------------------------------------------------------
# EXERCISE 4 — Compute totals (convert strings to numbers first)
# ---------------------------------------------------------------------------
print("=== Exercise 4: Totals ===")
total_revenue = 0.0
with open(SALES_FILE, "r") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        product = row[0]
        price = float(row[1])
        quantity = int(row[2])
        line_total = price * quantity
        total_revenue += line_total
        print(f"{product}: {quantity} units × ${price:.2f} = ${line_total:.2f}")
print(f"Total revenue: ${total_revenue:,.2f}")
print()

# ---------------------------------------------------------------------------
# EXERCISE 5 — Filter orders over $100 and write data/cleaned.csv
# ---------------------------------------------------------------------------
print("=== Exercise 5: Filter and write ===")
original_count = 0
written_count = 0
with open(SALES_FILE, "r") as infile, open(CLEANED_FILE, "w", newline="") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    next(reader)
    writer.writerow(["Product", "Price", "Qty", "Total"])
    for row in reader:
        original_count += 1
        price = float(row[1])
        quantity = int(row[2])
        line_total = price * quantity
        if line_total > 100:
            writer.writerow([row[0], f"{price:.2f}", quantity, f"{line_total:.2f}"])
            written_count += 1
print(f"Wrote {written_count} of {original_count} rows to {CLEANED_FILE}")
print()

# ---------------------------------------------------------------------------
# EXERCISE 6 — Same totals using csv.DictReader (access columns by name)
# ---------------------------------------------------------------------------
# csv.reader gives each row as a list, so you use positions like row[1]; it's simple
# and fine for small files whose column order never changes.
# csv.DictReader uses column names like row["price"], which is easier to read and
# keeps working if columns get reordered or added, so I'd prefer it for real data.
print("=== Exercise 6: DictReader ===")
dict_total = 0.0
with open(SALES_FILE, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        price = float(row["price"])
        quantity = int(row["quantity"])
        line_total = price * quantity
        dict_total += line_total
        print(f"{row['product']}: {quantity} units × ${price:.2f} = ${line_total:.2f}")
print(f"Total revenue: ${dict_total:,.2f}")
print("Matches Exercise 4:", round(dict_total, 2) == round(total_revenue, 2))
print()

# ---------------------------------------------------------------------------
# EXERCISE 7 — Summary dictionary {product: total_revenue}
# ---------------------------------------------------------------------------
print("=== Exercise 7: Sales summary by product ===")
summary = {}
with open(SALES_FILE, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        product = row["product"]
        line_total = float(row["price"]) * int(row["quantity"])
        # .get(product, 0) starts a new product at 0, then adds to it
        summary[product] = summary.get(product, 0) + line_total

for product in sorted(summary):
    print(f"{product}: ${summary[product]:,.2f}")
print()

# ---------------------------------------------------------------------------
# EXERCISE 8 — Append one line per run to data/run_log.txt
# ---------------------------------------------------------------------------
print("=== Exercise 8: Append mode log ===")
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(LOG_FILE, "a") as log:   # "a" adds to the end instead of overwriting
    log.write(f"{timestamp} | Total revenue: ${total_revenue:,.2f}\n")

with open(LOG_FILE, "r") as log:
    entries = log.readlines()
print(f"Logged run at {timestamp}. {LOG_FILE} now has {len(entries)} entries.")
