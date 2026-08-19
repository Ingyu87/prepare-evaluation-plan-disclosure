#!/usr/bin/env python3
"""내장된 2022 개정 교육과정 성취기준별 A·B·C 성취수준을 조회한다."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys


DATA_PATH = Path(__file__).resolve().parents[1] / "references" / "official-achievement-levels-2022.json"
CODE_RE = re.compile(r"^(?:2|4|6)[가-힣]+\d{2}-\d{2}$")
LABELS = {"A": "잘함", "B": "보통", "C": "노력요함"}


def band_for(code: str) -> str:
    return {"2": "1-2", "4": "3-4", "6": "5-6"}[code[0]]


def load_data() -> dict:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def lookup(codes: list[str]) -> tuple[list[dict], list[str]]:
    data = load_data()
    records: list[dict] = []
    missing: list[str] = []
    for raw_code in codes:
        code = raw_code.strip().strip("[]")
        if not CODE_RE.fullmatch(code):
            missing.append(code)
            continue
        band = band_for(code)
        levels = data["bands"][band].get(code)
        if levels is None:
            missing.append(code)
            continue
        records.append(
            {
                "code": code,
                "band": band,
                "잘함": levels["A"],
                "보통": levels["B"],
                "노력요함": levels["C"],
            }
        )
    return records, missing


def combined(records: list[dict]) -> dict[str, str]:
    result: dict[str, str] = {}
    for label in LABELS.values():
        unique: list[str] = []
        for record in records:
            sentence = record[label]
            if sentence not in unique:
                unique.append(sentence)
        result[label] = " ".join(unique)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="공식 성취기준별 성취수준 조회")
    parser.add_argument("codes", nargs="+", help="성취기준 코드(예: 2국01-01)")
    parser.add_argument("--combine", action="store_true", help="여러 코드의 단계별 문장을 코드 순서대로 결합")
    args = parser.parse_args()

    records, missing = lookup(args.codes)
    output: dict = {"records": records, "missing": missing}
    if args.combine:
        output["combined"] = combined(records)
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 2 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
