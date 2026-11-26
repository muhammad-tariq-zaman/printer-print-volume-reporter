# printer-print-volume-reporter

Report pages printed per printer per month from a CSV: the input CSV lists printer, month and pages — each printer-month is reported heaviest first, followed by a total per printer and a grand total. Rows with a non-numeric pages value are reported as skipped, not silently dropped.

Sample input is included (sample.csv with six rows, one invalid row).

## How to run

```sh
python3 main.py sample.csv
```

## Example output

```
PRN-03 2026-10: 2100 page(s)
PRN-01 2026-10: 1450 page(s)
PRN-01 2026-09: 1200 page(s)
PRN-02 2026-10: 950 page(s)
PRN-02 2026-09: 800 page(s)
TOTAL PRN-01: 2650 page(s)
TOTAL PRN-03: 2100 page(s)
TOTAL PRN-02: 1750 page(s)
Grand total: 6500 page(s) across 5 printer-month(s).
Skipped 1 invalid row(s).
```

Standard library only. Run the tests with `python3 -m unittest discover`.
