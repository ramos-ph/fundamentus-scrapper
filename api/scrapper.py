import re
from stocks_scrapper import get_stocks_payment_dates
from errors import ScrapError

REAL_ESTATE_SYMBOL_PATTERN = r'\w{4}11'

def get_payment_dates(symbols):
	payments = []
	errors = []

	for symbol in symbols:
		try:
			result = get_stocks_payment_dates(symbol)
			payments.append(result)
		except ScrapError as e:
			errors.append(e.message)

	return [payments, errors]


def is_symbol_real_estate(symbol):
	return re.match(REAL_ESTATE_SYMBOL_PATTERN, symbol)
