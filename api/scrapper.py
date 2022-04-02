import re
import pandas as pd
from datetime import datetime
from real_estate_scrapper import get_real_estate_payment_dates
from stocks_scrapper import get_stock_payment_dates

REAL_ESTATE_PATTERN = r'\w{4}11'
DATE_PATTERN = '\d{2}/\d{2}/\d{4}'
COLUMNS = ['symbol', 'date', 'payment', 'value', 'type']

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

def format_payments_to_json(df):
	symbols = list(df['symbol'].drop_duplicates())
	payments = []
	for symbol in symbols:
		payments.append(get_pending_earnings_for(symbol, df))
	return payments

def get_pending_earnings_for(symbol, df):
	df = df[(df['symbol'] == symbol) & (df['payment'].str.contains(DATE_PATTERN))]
	df = df.assign(payment_timestamp=pd.to_datetime(df['payment'], format='%d/%m/%Y'))
	df = df[df['payment_timestamp'] >= datetime.now()]

	return {
		'symbol': symbol,
		'earnings': df[['value', 'payment', 'type']].to_dict(orient='records')
	}
