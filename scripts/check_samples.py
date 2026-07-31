#!/usr/bin/env python3
"""Parse all committed SMS samples and fail if any template is unknown."""

import json
import sys
from pathlib import Path

from realize import alinma_parse, alrajhi_parse


ROOT = Path(__file__).resolve().parent.parent
SAMPLE_CHECKS = {
    "alinma": (ROOT / "samples" / "alinma_sms.json", alinma_parse),
    "alrajhi": (ROOT / "samples" / "alrajhi_sms.json", alrajhi_parse),
}


def check_bank(bank, sample_path, parser):
    try:
        with sample_path.open(encoding="utf-8") as file:
            messages = json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        print(f"{bank}: could not load {sample_path}: {error}", file=sys.stderr)
        return 0, 0, 0, 1

    if not isinstance(messages, list):
        print(f"{bank}: sample file must contain a JSON list", file=sys.stderr)
        return 0, 0, 0, 1

    parsed = 0
    ignored = 0
    unknown = 0
    errors = 0

    for index, message in enumerate(messages, start=1):
        try:
            result = parser(message)
        except Exception as error:
            errors += 1
            print(f"\n[{bank} sample {index}] parser error: {error}", file=sys.stderr)
            print(message.get("text", repr(message)), file=sys.stderr)
            continue

        if result is None:
            ignored += 1
        elif isinstance(result, dict) and result.get("type") == "unknown":
            unknown += 1
            print(f"\n[{bank} sample {index}] unknown template:", file=sys.stderr)
            print(message.get("text", repr(message)), file=sys.stderr)
        elif isinstance(result, dict):
            parsed += 1
        else:
            errors += 1
            print(
                f"\n[{bank} sample {index}] invalid parser result: {result!r}",
                file=sys.stderr,
            )

    print(
        f"{bank}: {len(messages)} total, {parsed} parsed, "
        f"{ignored} ignored, {unknown} unknown, {errors} errors"
    )
    return len(messages), parsed, unknown, errors


def main():
    total_unknown = 0
    total_errors = 0

    for bank, (sample_path, parser) in SAMPLE_CHECKS.items():
        _, _, unknown, errors = check_bank(bank, sample_path, parser)
        total_unknown += unknown
        total_errors += errors

    if total_unknown or total_errors:
        print(
            f"Sample check failed: {total_unknown} unknown, {total_errors} errors.",
            file=sys.stderr,
        )
        return 1

    print("Sample check passed: no unknown templates or parser errors.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
