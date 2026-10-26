# Banks SMS Messages Analyzer

[![Check SMS samples](https://github.com/Muaath5/bank_sms_parser/actions/workflows/check-samples.yml/badge.svg)](https://github.com/Muaath5/bank_sms_parser/actions/workflows/check-samples.yml)

A script that fetches SMS messages from an Android phone and analyzes supported bank messages to produce JSON and CSV transaction data.

## Supported Banks

- Al Rajhi (`AlRajhiBank`)
- Alinma (`alinma`)

Template samples are available in the `samples/` folder.

## Features

- Pulls an SMS backup from an Android phone.
- Converts supported bank messages to JSON.
- Extracts information such as `type`, `ingoing`/`outgoing`, `amount`, `from`/`to`, and `at`.
- Produces a CSV file for analysis.

## Requirements

- `adb`
- USB debugging enabled on the Android phone
- Python 3.8+

## Usage

```sh
git clone https://github.com/Muaath5/bank_sms_parser.git
cd bank_sms_parser
./run.sh
```

## Checking SMS Samples

The sample checker uses only the Python standard library. It parses every committed sample and fails when a parser raises an error or returns an unknown template.

```sh
python3 scripts/check_samples.py
```

Informational messages such as verification codes and account notices are counted as ignored. Supported financial messages are counted as parsed.

## Currency Conversion

Fixed conversion rates are stored in `scripts/exchange_rates.py`. They are project defaults and are not live exchange rates.

## Merchant Classification

In `./data/merchants.json`, you can assign different merchant titles to the same company and add a three-letter classification suffix. For example, `SAUDI ARABIAN` and `SAUDI AIRLINES` can both map to `saudia_trn`.

The current possible classes are:

```py
CLASSES = {
    "tls": "Tools",
    "mkt": "Supermarkets",
    "rst": "Restaurants",
    "onl": "Online",
    "chr": "Donation",
    "inv": "Invest",
    "gov": "Gov",
    "tea": "Drinks",
    "gas": "Gas",
    "lnd": "Laundry",
    "clt": "Clothing",
    "trn": "Transport",
    "net": "Internet",
    "srv": "Services",
    "cld": "Cloud",
    "phr": "Pharmacy",
    "hlt": "Health",
    "idk": "Unknown"
}
```

You can also use `manual_classification.json`:

```json
{
    "1780098870_abcdef": "Internet",
    "1784810195_3e9fde": "Gas"
}
```

## Output

### `summary.json`

- `id`: unique ID in the format `{unix_timestamp}_{sms_message_hash_6_letters}`
- `sms_bank`: currently either `alinma` or `AlRajhiBank`
- `sms_text`: original SMS text
- `sms_date`: SMS date in `yyyy-mm-dd hh:MM:ss` format

Optional fields depend on the message type:

- `flow`: either `ingoing` or `outgoing`
- `type`: `buy`, `buy_internet`, `transaction`, or another supported type
- `amount`: amount converted to SAR
- `for`: merchant name
- `from`: source
- `to`: destination
- `at`: date and time included in the bank SMS

### `operations.csv`

Headers:

- `id`
- `date`
- `amount`
- `type`
- `assigned`
- `bank`
- `classification`

## Resources

- [SAMA Standards for SMS notifications](https://rulebook.sama.gov.sa/en/standardization-notification-elements-sent-financial-institutions-customers)

## License

Copyright (C) 2026 Muaath Alqarni.

Licensed under the GNU Affero General Public License v3.0 only (`AGPL-3.0-only`). Distributed forks and modified versions must follow the license's source-sharing requirements. See `LICENSE` for the full terms.
