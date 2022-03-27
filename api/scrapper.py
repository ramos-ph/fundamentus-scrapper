import requests
import re
from bs4 import BeautifulSoup

ROWS_SEPARATORS_RE = r'\n|(?<=\d{2}/\d{2}/\d{4})\s'

def get_stocks_payment_dates(symbols):
	payments = []
	errors = []

	for symbol in symbols:
		request_url = f'https://www.fundamentus.com.br/proventos.php?tipo=2&papel={symbol}'

		try:
			html = requests.get(request_url, headers={'User-Agent': 'Mozilla/5.0'})
			payments.append(scrap_html(html.text, symbol))
		except:
			errors.append(symbol)

	return [payments, errors]


def scrap_html(html, symbol):
	soup = BeautifulSoup(html, 'html.parser')
	table = soup.find(id='resultado')

	rows = []
	for tableRow in table.tbody:
		if not tableRow == '\n':
			_, value, type, date, _ = parse_rows_to_array(tableRow)
			rows.append([symbol, value, type, date])
	return rows


def parse_rows_to_array(tableRow):
	content = re.split(ROWS_SEPARATORS_RE, tableRow.text)
	return [tableRow for tableRow in content if tableRow]
