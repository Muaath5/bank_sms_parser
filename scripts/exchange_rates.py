"""Fixed currency conversion rates used by the SMS parser.

Values convert one unit of the listed currency to Saudi riyals. These are
project defaults, not live exchange rates.
"""

CURRENCY_RATES = {
    "SR": 1,
    "SAR": 1,
    "ريال": 1,
    "USD": 3.75,
    "AED": 1,
    "MKD": 0.07,
    "EGP": 0.13,
    "MDL": 0.21,
    "CNY": 0.55,
}
