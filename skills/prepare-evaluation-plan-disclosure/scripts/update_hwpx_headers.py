#!/usr/bin/env python3
"""정보공시용 평가계획 HWPX의 새 양식 표제를 공식 표현으로 바꾼다."""

from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZipFile


TEXT_REPLACEMENTS = {
    "<hp:t>평가 방법</hp:t>": "<hp:t>평가 방법 및 횟수</hp:t>",
    "<hp:t>(교수학습내용)</hp:t>": "<hp:t>(교수·학습 내용)</hp:t>",
    "<hp:t>(교수 학습 내용)</hp:t>": "<hp:t>(교수·학습 내용)</hp:t>",
    "<hp:t>(교수·학습내용)</hp:t>": "<hp:t>(교수·학습 내용)</hp:t>",
}


def patch_text(text: str) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    for old, new in TEXT_REPLACEMENTS.items():
        count = text.count(old)
        if count:
            text = text.replace(old, new)
        counts[old] = count
    return text, counts


def patch_preview(text: str) -> str:
    text = text.replace("<평가 방법>", "<평가 방법 및 횟수>")
    for old in ("(교수학습내용)", "(교수 학습 내용)", "(교수·학습내용)"):
        text = text.replace(old, "(교수·학습 내용)")
    return text


def update_hwpx(source: Path, target: Path, allow_noop: bool) -> int:
    if source.resolve() == target.resolve():
        raise ValueError("원본과 결과 경로는 달라야 합니다.")
    if not source.is_file():
        raise FileNotFoundError(source)

    target.parent.mkdir(parents=True, exist_ok=True)
    changed = 0

    with ZipFile(source, "r") as src, ZipFile(target, "w") as dst:
        for info in src.infolist():
            data = src.read(info.filename)

            if info.filename.startswith("Contents/section") and info.filename.endswith(".xml"):
                text, counts = patch_text(data.decode("utf-8"))
                changed += sum(counts.values())
                data = text.encode("utf-8")
            elif info.filename == "Preview/PrvText.txt":
                data = patch_preview(data.decode("utf-8")).encode("utf-8")

            dst.writestr(info, data)

    if changed == 0 and not allow_noop:
        target.unlink(missing_ok=True)
        raise RuntimeError("변경할 새 양식 표제를 찾지 못했습니다. --allow-noop으로 무변경 복사를 허용할 수 있습니다.")

    return changed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    parser.add_argument("--allow-noop", action="store_true")
    args = parser.parse_args()

    changed = update_hwpx(args.source, args.target, args.allow_noop)
    print(f"Updated {changed} header text node(s): {args.target}")


if __name__ == "__main__":
    main()
