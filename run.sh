#!/bin/sh
set -e

if [ ! -d "data" ]; then
    mkdir data
    echo "Made ./data/"
else
    echo "./data/ Already exists"
fi

adb devices          
adb shell content query --uri content://sms/ > ./data/sms_backup.txt
python3 ./scripts/parser.py ./data/sms_backup.txt
python3 ./scripts/realize.py
python3 ./scripts/tablize.py
