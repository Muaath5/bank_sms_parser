import json
import datetime
import re
import hashlib

NAME='asdf'
ALRAJHI_ACCOUNT=1234

DATA_FOLDER='./data'
OUTPUT_FILE='summary.json'


def get_6char_hex_hash(input_string):
    full_hash = hashlib.sha256(input_string.encode('utf-8')).hexdigest()
    return full_hash[:6]


def extract_number(text: str) -> float:
    try:
        parts = text.strip().split(' ')
        currency = {
            'SR': 1,
            'SAR': 1,
            'ريال': 1,


            'USD': 3.75, # USA
            'AED': 1,    # UAE
            'MKD': 0.07, # Macedonia
            'EGP': 0.13, # Egypt
            'MDL': 0.21, # Moldova
            'CNY': 0.55, # China
        }
        if parts[0] in currency:
            parts[0], parts[1] = parts[1], parts[0]
        parts[0] = parts[0].replace(',', '')
        return float(parts[0]) * currency[parts[1]]
    except:
        print(f"Invalid extract_number call: {text}")
        exit(1)

def realize(bank):
    with open(f"sms_backup_{bank}.json", 'r') as f:
        data = json.load(f)
    head = set()
    for d in data:
        # print()
        head.add(d['text'].split('\n')[0])
        # break
    head = sorted(head)
    for h in head:
        print(h)

def construct_labels(lines, titles):
    labels = {}
    for x, y in titles:
        labels[y] = None
    for ln in lines:
        for x, y in titles:
            if ln.strip().startswith(x):
                labels[y] = ln.replace(x, "")
                break
    return labels

def alinma_parse(msg):
    lines = msg['text'].split('\n')
    top = lines[0].strip()

    if top.startswith('Please use the activation code') or top.startswith('رمز شراء أونلاين') or 'لا يكفي لإتمام مشترياتك' in top or top == 'لإتمام عملية الشراء عبر الإنترنت' or top.startswith('استخدم رمز التفعيل:') or top.startswith('عميلنا العزيز') or top.startswith('رمز التفعيل:'):
        return None

    labels = construct_labels(lines, [
        ('مبلغ: ', "amount"),
        ('في: ', "at"),
        ('بطاقة: ', "card"),
        ('من: ', "from"),
        ('الى: ', "to")
    ])


    if top == 'تم إيداع الراتب':
        labels = construct_labels(lines, [
            ('مبلغ ', "amount"),
            ('في', "at"),
            ('لـ ', "account"),
        ])
        return {
            "flow": "ingoing",
            "type": "payroll",
            "amount": extract_number(labels["amount"]),
            "at": labels["at"],
            "account": labels["account"]
        }

    if top.startswith('تم قيد مبلغ'):
        return {
            "flow": "ingoing",
            "type": "income",
            "amount": float(top.split(' ')[3]),
            "account": top.split(' ')[5]
        }

    if top == f'هلا {NAME}':
        if lines[1] == 'تم إيداع الراتب':
            labels = construct_labels(lines, [
                ('بمبلغ: ', "amount"),
                ('في: ', "at"),
                ('في حساب: ', "account"),
            ])
            return {
                "flow": "ingoing",
                "type": "payroll",
                "amount": extract_number(labels["amount"]),
                "at": labels["at"],
                "account": labels["account"]
            }
        else:
            return None

    if top == 'شراء (مدى Pay)':
        return {
            "flow": "outgoing",
            "type": "buy",
            "amount": extract_number(labels['amount']),
            "from": labels["from"],
            "at": labels["at"]
        }
    if top == 'حوالة عكسية':
        labels = construct_labels(lines, [
            ('مبلغ: ', "amount"),
            ('في: ', "at"),
            ('لبطاقة مدى: ', "card"),
            ('من البائع: ', "from"),
            ('الحساب: ', "to")
        ])
        return {
            "flow": "ingoing",
            "type": "reversal_transaction",
            "amount": extract_number(labels['amount']),
            "from": labels["from"],
            "card": labels["card"],
            "to": labels['to'],
            "at": labels["at"]
        }
    if top == 'شراء عبر نقاط البيع':
        labels = construct_labels(lines, [
            ('مبلغ ', "amount"),
            ('في ', "at"),
            ('بطاقة مدى:', "card"),
            ('من ', "from"),
        ])
        return {
            "flow": "outgoing",
            "type": "buy",
            "amount": extract_number(labels['amount']),
            "from": labels["from"],
            "at": labels["at"]
        }
    if top == 'شراء عبر نقاط بيع':
        labels = construct_labels(lines, [
            ('مبلغ ', "amount"),
            ('في ', "at"),
            ('بطاقة ', "card"),
            ('من ', "from"),
        ])
        return {
            "flow": "outgoing",
            "type": "buy",
            "amount": extract_number(labels['amount']),
            "from": labels["from"],
            "card": labels["card"],
            "at": labels["at"]
        }
    if top == 'شراء إنترنت':
        if "مبلغ:" not in msg['text']:
            labels['amount'] = next((l.replace("مبلغ ", "").strip() for l in lines if l.startswith("مبلغ ")), "")
        return {
            "flow": "outgoing",
            "type": "buy_internet",
            "amount": extract_number(labels['amount']),
            "from": labels["from"],
            "at": labels["at"]
        }
    if top.startswith('شراء إنترنت'):
        labels['amount'] = top[12:]
        return {
            "flow": "outgoing",
            "type": "buy_internet",
            "amount": extract_number(labels['amount']),
            "from": labels["from"],
            "at": labels["at"]
        }
    if top == 'حوالة واردة داخلية' or top == 'حوالة واردة محلية سريع':
        labels = construct_labels(lines, [
            ('المبلغ: ', "amount"),
            ('في: ', "at"),
            ('لحساب: ', "account"),
            ('من: ', "from"),
            ('الى: ', "to")
        ])
        return {
            "flow": "ingoing",
            "type": "transaction",
            "amount": extract_number(labels['amount']),
            "from": labels["from"],
            "account": labels["account"],
            "at": labels["at"]
        }
    if top == 'حوالة واردة محلية':
        labels = construct_labels(lines, [
            ('مبلغ ', "amount"),
            ('في ', "at"),
            ('حساب ', "account"),
            ('من ', "from")
        ])
        return {
            "flow": "ingoing",
            "type": "transaction",
            "amount": extract_number(labels['amount']),
            "from": labels["from"],
            "at": labels["at"],
            "account": labels["account"]
        }
    if top == 'حوالة صادرة لحسابك الاستثماري في بنك الانماء':
        return {
            "flow": "outgoing",
            "type": "investment",
            "amount": extract_number(labels['amount']),
            "from": labels["from"],
            "at": labels["at"]
        }
    if top == 'حوالة صادرة داخلية':
        if 'لـ' in msg['text']:
            labels = construct_labels(lines, [
                ('مبلغ ', "amount"),
                ('في ', "at"),
                ('لحساب ', "account"),
                ('لـ ', "to")
            ])
        else: 
            labels = construct_labels(lines, [
                ('مبلغ: ', "amount"),
                ('في: ', "at"),
                ('لحساب: ', "account"),
                ('من حساب: ', "from"),
                ('المستفيد: ', "to")
            ])
        return {
            "flow": "outgoing",
            "type": "transaction",
            "amount": extract_number(labels['amount']),
            "account": labels["account"],
            "to": labels["to"],
            "at": labels["at"]
        }
    return {"type": "unknown"}

def alrajhi_parse(msg):
    lines = msg['text'].split('\n')
    top = lines[0].strip()

    if top == 'عزيزي العميل,' or top.startswith('تم تسجيل الدخول إلى حسابك من جهاز جديد') or top.startswith('OTP Code') or top.startswith('تمت اضافة المستفيد') or top.startswith('تم تنشيط المستفيد') or top.startswith('نظرا لعدم وجود رصيد') or top == 'كلمة مرور لمرة واحدة' or top.startswith('كلمة مرور صالحة لمرة واحدة') or top.startswith('رمز مؤقت') or top.startswith('رمز التحقق') or top == 'ننصح بعدم مشاركة الرمز لحمايتك من الاحتيال' or top.startswith('اشعار:'):
        return None

    if re.match("Your card [0-9]{4}", top):
        return None
    
    if top == 'يرجى تحديث هويتك لتفادي ايقاف حسابك':
        return None

    if 'بإمكانكم تجديد البطاقة من خلال أجهزة الخدمة الذاتية' in top:
        return None
    
    if top.startswith("عزيزي") or top.startswith('عميلنا العزيز،'):
        return None

    if top == 'حوالة مالية صادرة مرفوضة':
        return None

    labels = construct_labels(lines, {
        ('لدى:', 'for'),
        ('من:', 'from'),
        ('الى:', 'to'),
        ('مبلغ:', 'amount'),
        ('بطاقة:', 'card'),
        ('في:', 'at'),
        ('عبر:', 'via'),
        ('الجهة:', 'department'),
        ('الخدمة:', 'service'),
        ('دولة:', 'country'),
        ('مكان السحب:', 'place'),
    })
    if top == 'شراء':
        if 'بـ' in msg["text"]:
            labels = construct_labels(lines, {
                ('لـ', 'for'),
                ('بـ', 'amount'),
                ('عبر:', 'card'),
                ('؜', 'at')
            })
        return {
            "flow": "outgoing",
            "type": "buy",
            "amount": extract_number(labels["amount"]),
            "for": labels["for"],
            "date": msg["date"],
            "card": labels["card"],
            "at": labels["at"]
        }
    
    if top == 'حوالة بين حساباتك':
        return {
            "type": "internal_transaction",
            "amount": extract_number(labels["amount"]),
            "to": labels["to"]
        }
    if top == 'راتب':
        return {
            "flow": "ingoing",
            "type": "payroll",
            "amount": extract_number(labels['amount']),
            "to": labels["to"],
            "at": labels["at"]
        }
    if top == 'ﺷراء':
        labels = construct_labels(lines, {
            ('ﻟدى:', 'for'),
            ('ﻣن:', 'from'),
            ('اﻟﻰ:', 'to'),
            ('ﻣﺑﻟﻎ:', 'amount'),
            ('ﺑطﺎﻗة:', 'card'),
            ('ﻓﻲ:', 'at')
        })
        
        return {
            "type": "buy",
            "amount": extract_number(labels["amount"]),
            "for": labels["for"],
            "card": labels["card"],
            "at": labels["at"]
        }
    if top == 'تفويض عبر الانترنت':
        return {
            "flow": "outgoing",
            "type": "hold",
            "amount": extract_number(labels["amount"]),
            "for": labels["for"],
            "card": labels["card"],
            "at": labels["at"]   
        }
    if top == 'خصم من التفويض عبر الانترنت':
        return {
            "flow": "outgoing",
            "type": "buy_hold",
            "amount": extract_number(labels["amount"]),
            "for": labels["for"],
            "card": labels["card"],
            "at": labels["at"]   
        }
    if top == 'سحب:صراف آلي':
        return {
            "flow": "outgoing",
            "type": "withdrawal",
            "amount": extract_number(labels["amount"]),
            "place": labels["place"],
            "card": labels["card"],
            "at": labels["at"]
        }
    if top == 'ايداع شيك ورقي':
        return {
            "flow": "ingoing",
            "type": "deposit",
            "amount": extract_number(labels['amount']),
            "to": labels["to"],
            "note": "cheque"
        }
    if top == 'إيداع:صراف آلي':
        return {
            "flow": "ingoing",
            "type": "deposit",
            "amount": extract_number(labels["amount"]),
            "to": labels["to"],
            "at": labels["at"]
        }
    if top == 'سداد فاتورة':
        return {
            "flow": "outgoing",
            "type": "sadad",
            "amount": extract_number(labels["amount"]),
            "from": labels["from"],
            "service": labels["service"],
        }
    if top == 'شراء دولي':
        return {
            "flow": "outgoing",
            "type": "international_payment",
            "amount": extract_number(labels["amount"]),
            "card": labels["card"],
            "country": labels["country"],
            "for": labels["for"]
        }
    if top == 'مدفوعات وزارة الداخلية':
        return {
            "flow": "outgoing",
            "type": "moi_payment",
            "amount": extract_number(labels["amount"]),
            "from": labels["from"],
            "department": labels["department"],
        }
    if top == 'شراء انترنت':
        return {
            "flow": "outgoing",
            "type": "buy_internet",
            "amount": extract_number(labels["amount"]), 
            "for": labels["for"],
            "card": labels["card"]
        }
    if top == 'استرداد شراء':
        return {
            "flow": "ingoing",
            "type": "buy_reget",
            "amount": extract_number(labels["amount"]),
            "for": labels["for"]
        }
    if top == 'استرداد شراء الانترنت':
        return {
            "flow": "ingoing",
            "type": "buy_internet_reget",
            "amount": extract_number(labels["amount"]),
            "for": labels["for"]
        }
    if top == 'حوالة داخلية' or top == 'حوالة محلية':

        return {
            "flow": ("outgoing" if labels["from"] == str(ALRAJHI_ACCOUNT) else "ingoing"),
            "type": "transaction",
            "amount": extract_number(labels["amount"]),
            "from": labels["from"],
            "to": labels['to']
        }
    if top == 'عملية شراء-حساب جاري - المتجر الألكتروني':
        return {
            "flow": "outgoing",
            "type": "buy",
            "amount": extract_number(labels["amount"]),
            "from": labels["from"]
        }
    if top.startswith('حوالة داخلية واردة بـ'):
        labels = construct_labels(lines, {
            ('من', 'from'),
            ('لـ', 'to'),
            ('بـ', 'amount')
        })
        labels["amount"] = top.split('بـ')[1]
        return {
            "flow": "ingoing",
            "type": "transaction",
            "amount": extract_number(labels["amount"]),
            "from": labels["from"],
            "to": labels['to']
        }
    if top == 'حوالة محلية صادرة':
        return {
            "flow": "outgoing",
            "type": "transaction",
            "amount": extract_number(labels["amount"]),
            "from": labels["from"],
            "to": labels['to'],
            "via": labels['via']
        }
    if top == 'حوالة داخلية صادرة':
        return {
            "flow": "outgoing",
            "type": "transaction",
            "amount": extract_number(labels["amount"]),
            "from": labels["from"],
            "to": labels['to'],
            "via": labels['via']
        }
    if top == 'إيداع دعم حكومي - حساب المواطن':
        labels = construct_labels(lines, {
            ('لدى:', 'for'),
            ('من:', 'from'),
            ('الى:', 'to'),
            ('المبلغ:', 'amount'),
            ('بطاقة:', 'card'),
            ('في:', 'at'),
            ('عبر:', 'via'),
            ('الجهة:', 'department'),
            ('الخدمة:', 'service'),
            ('دولة:', 'country'),
            ('مكان السحب:', 'place'),
        })
        return {
            "flow": "ingoing",
            "type": "citzen_account",
            "amount": extract_number(labels["amount"]),
            "to": labels['to']
        }
    if top == 'حوالة داخلية واردة':
        if 'لـ' in msg['text']:
            labels = construct_labels(lines, {
                ('من', 'from'),
                ('لـ', 'to'),
                ('بـ', 'amount')
            })
            return {
                "flow": "ingoing",
                "type": "transaction",
                "amount": extract_number(labels["amount"]),
                "from": labels["from"],
                "to": labels['to']
            }
        else:
            return {
                "flow": "ingoing",
                "type": "transaction",
                "amount": extract_number(labels["amount"]),
                "from": labels["from"],
                "to": labels['to'],
                "via": labels['via']
            }
    if top == 'حوالة محلية واردة':
        return {
            "flow": "ingoing",
            "type": "transaction",
            "amount": extract_number(labels["amount"]),
            "from": labels["from"],
            "to": labels['to'],
            "via": labels['via']
        }
    if top == 'ﺣواﻟة داﺧﻟﻳة' or top == 'ﺣواﻟة ﻣﺣﻟﻳة':
        labels = construct_labels(lines, {
            ('ﻟدى:', 'for'),
            ('ﻣن:', 'from'),
            ('اﻟﻰ:', 'to'),
            ('ﻣﺑﻟﻎ:', 'amount'),
            ('ﺑطﺎﻗة:', 'card'),
            ('ﻓﻲ:', 'at')
        })
        return {
            "flow": ("outgoing" if labels["from"] == str(ALRAJHI_ACCOUNT) else "ingoing"),
            "type": "transaction",
            "amount": extract_number(labels["amount"]),
            "from": labels["from"],
            "to": labels['to']
        }
    return {"type": "unknown"}

def main():
    banks = {
        'alinma': alinma_parse, 
        'AlRajhiBank': alrajhi_parse
    }

    res = []
    unknown = 0
    cnt = 0
    for bank, func in banks.items():
        unknown = 0
        cnt = 0
        try:
            with open(f"{DATA_FOLDER}/sms_backup_{bank}.json", 'r') as f:
                msgs = json.load(f)
        except FileNotFoundError:
            print(f"Bank {bank} file doesn't exist (./data/sms_backup_{bank}.json)")
            continue
        for msg in msgs:
            record = {
                'id': f"{int(datetime.datetime.fromisoformat(msg['date']).timestamp())}_{get_6char_hex_hash(bank + msg['date'] + msg['text'])}",
                'sms_bank': bank,
                'sms_date': msg['date'],
                'sms_text': msg['text']
            }
            realized = func(msg)
            if realized is not None:
                record.update(realized)
                if record['type'] == 'unknown':
                    unknown += 1
                cnt += 1

                res.append(record)

        print(f"{bank}: {len(msgs)} total SMS messages, ({cnt - unknown}/{cnt}) = {(cnt - unknown)/cnt*100:.2f}%")
    res.sort(key=lambda x: x['sms_date'])

    with open(f'{DATA_FOLDER}/{OUTPUT_FILE}', 'w', encoding="utf-8") as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=4))
    print(f"Results saved to {OUTPUT_FILE}")

main()