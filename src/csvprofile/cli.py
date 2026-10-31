"""Command line entry point."""
import argparse
import json
import sys

from . import profile, read_csv


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="csvprofile", description="Profile a CSV file.")
    parser.add_argument("path")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    args = parser.parse_args(argv)
    try:
        rows, columns = read_csv(args.path)
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    report = profile(rows, columns)
    if args.json:
        print(json.dumps(report, indent=2))
        return 0
    header = ["column", "type", "count", "nulls", "distinct", "min", "max", "mean"]
    table = [header] + [[str(r.get(h, "")) for h in header] for r in report]
    widths = [max(len(row[i]) for row in table) for i in range(len(header))]
    for row in table:
        print("  ".join(cell.ljust(w) for cell, w in zip(row, widths)).rstrip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
