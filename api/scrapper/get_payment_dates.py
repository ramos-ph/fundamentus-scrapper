import pandas as pd
import requests
from bs4 import BeautifulSoup

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
