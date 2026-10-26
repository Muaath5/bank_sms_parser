import json, csv, os

DATA_FOLDER = './data'

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
    "phr": "Pharmacy",
    "idk": "Unknown"
}

def read_json(filename):
    with open(filename, 'r') as f:
        return json.loads(f.read())
    
def main():
    operations = read_json(f"{DATA_FOLDER}/summary.json")
    merchants = {}
    if os.path.isfile(f"{DATA_FOLDER}/merchants.json"):
        merchants = read_json(f"{DATA_FOLDER}/merchants.json")

    manual = {}
    if os.path.isfile(f"{DATA_FOLDER}/manual_classification.json"):
        manual = read_json(f"{DATA_FOLDER}/manual_classification.json")

    rows = []
    for op in operations:
        if 'flow' in op:

            if op['id'] in manual:
                if manual[op['id']] is None:
                    continue

            row = [
                op['id'],
                op['sms_date'], 
                (-1 if op['flow'] == 'outgoing' else 1) * op['amount'],
                op['type'],
                op.get('from', op.get('for')),
                op['sms_bank'],
                "Unclassified"
            ]
            if op['flow'] == 'outgoing' and op['type'] == 'transaction':
                row[4] = op['to']
            if op['type'] == 'buy' or op['type'] == 'buy_internet':
                if row[4] is not None:
                    if row[4] not in merchants or merchants[row[4]] is None or merchants[row[4]] == "":
                        merchants[row[4]] = None
                    else:
                        row[4] = merchants[row[4]]
                        merch_class = row[4].split('_')[-1]
                        if merch_class in CLASSES:
                            row[6] = CLASSES[merch_class]
                        else:
                            row[6] = "Unclassified"
            row[6] = manual.get(op['id'], row[6])
            rows.append(row)

    rows.sort()
    with open(f"{DATA_FOLDER}/operations.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "date", "amount", "type", "assigned", "bank", "classification"])
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows in operations.csv")

    with open(f"{DATA_FOLDER}/merchants.json", "w", encoding='utf-8') as file:
        file.write(json.dumps(merchants, indent=4, ensure_ascii=False))
    print(f"Updated merchents.json with {len(merchants)}")

main()