import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import report

def row(printer, month, pages):
    return {"printer": printer, "month": month, "pages": str(pages)}

class TestPrintVolumeReporter(unittest.TestCase):
    def test_heaviest_first(self):
        r, _, _ = report([row("PRN-01", "2026-09", 1200),
                          row("PRN-02", "2026-09", 800),
                          row("PRN-03", "2026-10", 2100)])
        self.assertEqual([x[0][0] for x in r], ["PRN-03", "PRN-01", "PRN-02"])

    def test_same_printer_month_is_summed(self):
        r, totals, _ = report([row("PRN-01", "2026-09", 500),
                               row("PRN-01", "2026-09", 700)])
        self.assertEqual((r[0][1], totals), (1200, [("PRN-01", 1200)]))

    def test_printer_totals(self):
        _, totals, _ = report([row("PRN-01", "2026-09", 1200),
                               row("PRN-01", "2026-10", 1450),
                               row("PRN-02", "2026-09", 800)])
        self.assertEqual(totals, [("PRN-01", 2650), ("PRN-02", 800)])

    def test_months_are_kept_separate(self):
        r, _, _ = report([row("PRN-01", "2026-09", 1200),
                          row("PRN-01", "2026-10", 1450)])
        self.assertEqual(len(r), 2)

    def test_negative_pages_is_skipped(self):
        r, _, skipped = report([row("PRN-01", "2026-09", -5),
                                row("PRN-01", "2026-09", 100)])
        self.assertEqual((len(r), skipped), (1, 1))

    def test_invalid_row_is_skipped(self):
        r, _, skipped = report([row("PRN-01", "2026-09", "lots"),
                                row("PRN-02", "2026-09", 800)])
        self.assertEqual((len(r), skipped), (1, 1))

    def test_empty_input(self):
        self.assertEqual(report([]), ([], [], 0))
