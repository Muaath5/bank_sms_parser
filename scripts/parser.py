#!/usr/bin/env python3
import re
import json
import sys
from datetime import datetime

# ---- Configure which contacts/senders to extract ----
# Matching is case-insensitive substring match against the "address" field.
CONTACTS = ["alinma", "AlRajhiBank"]

# Matches things like ", address=" (used to split fields within one row)
KEY_RE = re.compile(r'(?:^|, )([a-zA-Z_][a-zA-Z0-9_]*)=')

# Matches the start of a new row, e.g. "Row: 123 " — used to split the whole
# file into rows instead of splitting by newline, since a message body can
# itself contain real newline characters.
ROW_SPLIT_RE = re.compile(r'(?m)^Row:\s*\d+\s*')


def parse_rows(full_text):
    """Split the entire file into rows and parse each into a dict of fields."""
    # re.split keeps everything between "Row: N " markers, including
    # embedded newlines from multiline message bodies.
    chunks = ROW_SPLIT_RE.split(full_text)

    rows = []
    for chunk in chunks:
        chunk = chunk.strip('\n')
        if not chunk.strip():
            continue

        matches = list(KEY_RE.finditer(chunk))
        if not matches:
            continue

        fields = {}
        for i, m in enumerate(matches):
            key = m.group(1)
            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(chunk)
            value = chunk[start:end]
            # Trim trailing ", " or "\n" left over from the split
            value = value.rstrip('\n')
            if value.endswith(', '):
                value = value[:-2]
            fields[key] = value
        rows.append(fields)
    return rows


def ms_to_datetime_str(ms_str):
    try:
        ms = int(ms_str)
        return datetime.fromtimestamp(ms / 1000).strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        return ms_str  # fallback: leave as-is if unparseable


def main():
    if len(sys.argv) < 2:
        print("Usage: python sms_parser.py sms_backup.txt")
        sys.exit(1)

    input_path = sys.argv[1]

    # One message list per contact
    results = {contact: [] for contact in CONTACTS}

    with open(input_path, "r", encoding="utf-8", errors="replace") as f:
        full_text = f.read()

    for fields in parse_rows(full_text):
        address = fields.get("address", "") or ""
        body = fields.get("body", "") or ""
        date_ms = fields.get("date", "")

        for contact in CONTACTS:
            if contact.lower() in address.lower():
                results[contact].append({
                    "date": ms_to_datetime_str(date_ms),
                    "text": body
                })
                break

    for contact, messages in results.items():
        # Sort chronologically just in case the dump wasn't ordered
        messages.sort(key=lambda m: m["date"])

        out_filename = f"./data/sms_backup_{contact}.json"
        with open(out_filename, "w", encoding="utf-8") as out:
            json.dump(messages, out, ensure_ascii=False, indent=2)

        print(f"{contact}: {len(messages)} messages written to {out_filename}")


if __name__ == "__main__":
    main()
