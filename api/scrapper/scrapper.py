import pandas as pd
import re

from .format_payments_to_json import format_payments_to_json
from .get_payment_dates import get_real_estate_payment_dates, get_stock_payment_dates

COLUMNS = ['symbol', 'date', 'payment', 'value', 'type']
REAL_ESTATE_PATTERN = r'\w{4}11'

def get_symbols_payment_dates(symbols):
	df = pd.DataFrame(columns=COLUMNS)
	for symbol in symbols:
		df = df.append(get_symbol_payment_dates(symbol))
	return format_payments_to_json(df)

def get_symbol_payment_dates(symbol):
	if is_real_estate(symbol):
		df = get_real_estate_payment_dates(symbol)
	else:
		df = get_stock_payment_dates(symbol)
	return df[COLUMNS]

def is_real_estate(symbol):
	return re.match(REAL_ESTATE_PATTERN, symbol)
