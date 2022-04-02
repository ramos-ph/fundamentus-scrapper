import pandas as pd
import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup

COLUMNS = ['symbol', 'date', 'payment', 'value', 'type']
DATE_PATTERN = '\d{2}/\d{2}/\d{4}'
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

def get_stock_payment_dates(symbol):
	return get_payment_dates(symbol,
		f'https://www.fundamentus.com.br/proventos.php?tipo=2&papel={symbol}',
		['symbol', 'date', 'value', 'type', 'payment', 'per_share'])

def get_real_estate_payment_dates(symbol):
	return get_payment_dates(symbol,
		f'https://www.fundamentus.com.br/fii_proventos.php?tipo=2&papel={symbol}',
		['symbol', 'date', 'type', 'payment', 'value'])

def get_payment_dates(symbol, url, columns):
	html = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
	data = scrap_html(html.text, symbol)
	return pd.DataFrame(columns=columns, data=data)

def scrap_html(html, symbol):
	soup = BeautifulSoup(html, 'html.parser')
	_, *rows = soup.find_all('tr')
	return scrap_rows(rows, symbol)

def scrap_rows(rows, symbol):
	data = []
	for row in rows:
		data.append([symbol] + scrap_row(row))
	return data

def scrap_row(row):
	return [element.text.strip() for element in row.find_all('td') if should_include(element.text)]

def should_include(element):
	return not (element == "\n"	or element.isspace())

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
