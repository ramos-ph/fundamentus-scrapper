import requests
import re
from bs4 import BeautifulSoup
from errors import ScrapError

NEW_LINE_OR_DATE_PATTERN = r'\n|(?<=\d{2}/\d{2}/\d{4})\s'

def get_stocks_payment_dates(symbol):
	request_url = f'https://www.fundamentus.com.br/proventos.php?tipo=2&papel={symbol}'

	try:
		html = requests.get(request_url, headers={'User-Agent': 'Mozilla/5.0'})
		return scrap_html(html.text, symbol)
	except:
		raise ScrapError(symbol)


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
	content = re.split(NEW_LINE_OR_DATE_PATTERN, tableRow.text)
	return [tableRow for tableRow in content if tableRow]
