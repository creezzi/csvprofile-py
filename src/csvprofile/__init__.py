"""Column profiling for CSV files."""
from __future__ import annotations

import csv
import statistics
from typing import Any, Dict, Iterable, List, Sequence

__all__ = ["profile", "infer_type"]

NULLS = {"", "na", "n/a", "null", "none", "nan"}


def infer_type(values: Iterable[str]) -> str:
    kinds = set()
    for v in values:
        try:
            int(v)
            kinds.add("int")
            continue
        except ValueError:
            pass
        try:
            float(v)
            kinds.add("float")
        except ValueError:
            return "str"
    if not kinds:
        return "empty"
    return "float" if "float" in kinds else "int"


def profile(rows: Sequence[Dict[str, str]], columns: Sequence[str]) -> List[Dict[str, Any]]:
    report = []
    for col in columns:
        raw = [(r.get(col) or "").strip() for r in rows]
        present = [v for v in raw if v.lower() not in NULLS]
        kind = infer_type(present)
        info: Dict[str, Any] = {
            "column": col, "type": kind, "count": len(raw),
            "nulls": len(raw) - len(present), "distinct": len(set(present)),
        }
        if kind in ("int", "float") and present:
            nums = [float(v) for v in present]
            info.update(min=min(nums), max=max(nums), mean=round(statistics.fmean(nums), 4))
        report.append(info)
    return report


def read_csv(path: str):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return list(reader), reader.fieldnames or []
