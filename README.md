# Banks SMS Messages Analyzer

A script that fetches all SMS messages from your Android phone and analyzes messages banks contacts for your financial management to produce a final JSON and CSV of your transactions.

## Supported Banks
- Alrajhi (`AlRajhiBank`)
- Alinma (`alinma`)

## Features
- Pulls an SMS backup from your Android phone
- Puts your bank contacts messages in JSON format
- Extracts information from SMS messages (`type`, `ingoing`/`outgoing`, `amount`, `from`/`to`, `at`)
- Puts important information in CSV file for your analysis

## Requirements
- `adb` Program
- Enable USB Debugging
- Python 3.8+

## Steps
```
git clone https://github.com/Muaath5/bank_sms_analyzer.git
cd bank_sms_analyzer
./script.sh
```

After that in `./data/merchants.json` you might change the names of the merchants you buy from buy giving two different titles same company name and along with a classification like `SAUDI ARABIAN` and `SAUDI AIRLINES` as `saudia_trn`.

And make the last part of the name a 3-letter marking for the classification of this operation which would be added in the CSV.

The current possible classes:
```py
CLASSES = {
    "tls": "Tools",
    "mkt": "Supermarkets",
    "rst": "Restaurants",
    "onl": "Online",
    "chr": "Dontation",
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
    "idk": "Unknown"
}
```

Also you are able to use `manual_classification.json` in the following format:
```json
{
    "1780098870_abcdef": "Internet",
    "1784810195_3e9fde": "Gas"
}
```

## Output
### `summary.json`
- `id`: String, a unique ID in format `{unix_timestamp}_{sms_message_hash_6_letters}`
- `sms_bank`: String, currently either `alinma` or `AlRajhiBank`
- `sms_text`: String, the plain SMS text
- `sms_date`: String, in format `yyyy-mm-dd hh:MM:ss`

Along with many optional fields depending on the message type:
- `flow`: String, either `ingoing` or `outgoing`
- `type`: String, one of: `buy`/`buy_internet`/`transaction`/.../`unknown`
- `amount`: Float, the amount in SAR
- `for`: String, The buying merchant name
- `from`: String, From
- `to`: String, 
- `at`: String, bank SMS date and time

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
Soon