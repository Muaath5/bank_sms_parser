import json, csv

DATA_FOLDER = './data'

def read_json(filename):
    with open(filename, 'r') as f:
        return json.loads(f.read())
    
def main():
    operations = read_json(f"{DATA_FOLDER}/summary.json")
    rows = []
    for op in operations:
        if 'flow' in op:
            rows.append([op['sms_date'], (-1 if op['flow'] == 'outgoing' else 1) * op['amount'], op['type'], op.get('from', op.get('for')), op['sms_bank']])

    rows.sort()
    with open(f"{DATA_FOLDER}/operations.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows in operations.csv")

main()