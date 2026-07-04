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

## Resources
- [SAMA Standards for SMS notifications](https://rulebook.sama.gov.sa/en/standardization-notification-elements-sent-financial-institutions-customers)

## License
Coming soon