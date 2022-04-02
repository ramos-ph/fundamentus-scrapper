import requests
from bs4 import BeautifulSoup
from errors import ScrapError

def get_real_estate_payment_dates(symbol):
	request_url = 'https://www.fundamentus.com.br/fii_proventos.php?tipo=2&papel={symbol}'
	raise ScrapError(symbol)
