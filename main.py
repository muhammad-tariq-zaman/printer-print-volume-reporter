"""Report pages printed per printer per month from a CSV.

Usage: python3 main.py volume.csv
CSV columns: printer,month,pages. Each printer-month is
reported heaviest first, followed by a total per printer and
a grand total. Rows with a non-numeric pages value are
reported as skipped, not silently dropped.
"""
import argparse, csv, sys

def report(rows):
    totals = {}
    per_printer = {}
    skipped = 0
    for row in rows:
        try:
            printer = row["printer"].strip()
            month = row["month"].strip()
            pages = int(row["pages"])
            if not printer or not month or pages < 0:
                raise ValueError("bad value")
        except (KeyError, AttributeError, ValueError, TypeError):
            skipped += 1
            continue
        key = (printer, month)
        totals[key] = totals.get(key, 0) + pages
        per_printer[printer] = per_printer.get(printer, 0) + pages
    out = sorted(totals.items(), key=lambda kv: (-kv[1], kv[0][0], kv[0][1]))
    printer_totals = sorted(per_printer.items(), key=lambda kv: (-kv[1], kv[0]))
    return out, printer_totals, skipped

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        results, printer_totals, skipped = report(list(csv.DictReader(f)))
    for (printer, month), pages in results:
        print(f"{printer} {month}: {pages} page(s)")
    for printer, pages in printer_totals:
        print(f"TOTAL {printer}: {pages} page(s)")
    grand = sum(pages for _, pages in printer_totals)
    print(f"Grand total: {grand} page(s) across "
          f"{len(results)} printer-month(s).")
    if skipped:
        print(f"Skipped {skipped} invalid row(s).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
